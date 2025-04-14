import requests
from django.shortcuts import render
from datetime import datetime
from django.http import JsonResponse, HttpResponse
import locale

def dashboard_view(request):
    # Obtendo os parâmetros da URL
    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')
    banco_selecionado = request.GET.get('database')
    empresa_selecionada=request.GET.get('empresa')
    total_notas_canceladas=0
    # Inicializando variáveis para evitar problemas de escopo
    
    resultado_json = []
    resultado_nf = []
    resultado_venda = []
    total_valor_nf = 0
    formatted_valor_nf = 0
    total_notas = 0
    total_notas_pendente = 0
    totalCFOP5124 = 0
    totalCFOP5902 = 0
    error_message = None

    if data_inicio is not None and data_fim is not None:
        try:
            # Convertendo os parâmetros de data para o formato 'dd-mm-yyyy'
            data_inicio = datetime.strptime(data_inicio, '%Y-%m-%d').strftime('%d-%m-%Y')
            data_fim = datetime.strptime(data_fim, '%Y-%m-%d').strftime('%d-%m-%Y')
        except ValueError:
            return JsonResponse({'error': 'Formato de data inválido'}, status=400)
    
    # Construindo a URL da API com os parâmetros filtrados
    api_url = f'https://sua-api-aki/nf?data_inicio={data_inicio}&data_fim={data_fim}'
    
    # Adicionando o banco selecionado à URL da API, se houver
    if banco_selecionado:
        api_url += f'&banco={banco_selecionado}&empresa={empresa_selecionada}'

    
    # Construindo a URL da API para obter os nomes dos bancos
    bancos_api_url = 'https://sua-api-aki/'
    bancos = []
    try:
        # Fazendo a requisição para a API para obter os nomes dos bancos
        response_bancos = requests.get(bancos_api_url)
        response_bancos.raise_for_status()  # Levanta um erro para códigos de status HTTP 4xx/5xx
        
        # Processando a resposta da API para os nomes dos bancos
        bancos = response_bancos.json()
        
        # Fazendo a requisição para a API de notas fiscais
        response_nf = requests.get(api_url)
        response_nf.raise_for_status()  # Levanta um erro para códigos de status HTTP 4xx/5xx
        
        # Processando a resposta da API de notas fiscais
        data = response_nf.json()
        
        # Verificando se os dados retornados são uma lista de notas fiscais
        if isinstance(data, list):
            resultado_nf = data  # Se a API retornar uma lista, assumimos que são notas fiscais
        else:
            resultado_json = data.get('resultado_json', [])
            resultado_nf = data.get('resultado_nf', [])
            resultado_venda = data.get('resultado_venda', [])
        
        # Calculando totais e formatando valores
        total_valor_nf = sum(float(nf['valorTotalNF']) for nf in resultado_nf if nf.get('status') == '100' )
        formatted_valor_nf = "{:,.2f}".format(total_valor_nf).replace(",", " ").replace(".", ",").replace(" ", ".")

        total_notas = sum(1 for nf in resultado_nf if nf.get('status') == '100')
        total_notas_pendente = sum(1 for nf in resultado_nf if nf.get('status') == '0')
        total_notas_canceladas = sum(1 for nf in resultado_nf if nf.get('status') == '101' or nf.get('status') == '102')
        
        totalCFOP5124 = sum(float(nf['valorTotalNF']) for nf in resultado_nf if nf.get('cfop') == '5124' or nf.get('cfop') == '6124'  and nf.get('status') == '100')
        totalCFOP5902 = sum(float(nf['valorTotalNF']) for nf in resultado_nf if nf.get('cfop') == '5902'or nf.get('cfop') == '6902' and nf.get('status') == '100')
        totalCFOP5124 = "{:,.2f}".format(totalCFOP5124).replace(",", " ").replace(".", ",").replace(" ", ".")
        totalCFOP5902 = "{:,.2f}".format(totalCFOP5902).replace(",", " ").replace(".", ",").replace(" ", ".")
       
    except requests.exceptions.RequestException as e:
        # Tratamento de erro de requisição para a API
        error_message = f"Erro na requisição para API: {str(e)}"
    
    except (KeyError, ValueError) as e:
        # Tratamento de KeyError se as chaves não existirem nos dados retornados
        error_message = f"Dados incompletos ou erro na resposta da API: {str(e)}"
    
    # Montando o contexto para passar para o template
    contexto = {
        'nomes_bancos': bancos,  # Passando os nomes dos bancos para o template
        'resultado_json': resultado_json,
        'resultado_nf': resultado_nf,
        'resultado_venda': resultado_venda,
        'total_valor_nf': total_valor_nf,
        'formatted_valor_nf': formatted_valor_nf,
        'total_notas': total_notas,
        'total_notas_pendente': total_notas_pendente,
        'total_notas_canceladas':total_notas_canceladas,
        'totalCFOP5124': totalCFOP5124,
        'totalCFOP5902': totalCFOP5902,
        'data_inicio': data_inicio,  # Passando de volta para o template
        'data_fim': data_fim,        # Passando de volta para o template
        'error_message': error_message,
        'banco_selecionado': banco_selecionado,  # Passando o banco selecionado para o template
    }
    
    return render(request, 'dashboard.html', contexto)


def acompanhar_op(request):
    if request.method == 'GET':
        banco_selecionado = request.GET.get('database')
        op_numero = request.GET.get('op')
        return_xml = request.GET.get('xml', 'false').lower() == 'true'

        cfop_groups = {}
        op_info = []
        quantidade_entrada_item = []
        error_message = None
        cfop_5902 = False
        cfop_5124 = False
        bancos_api_url = 'https://sua-api-aki/'
        bancos = []
        xml_available = False  # Adiciona a variável para verificar a disponibilidade do XML

        try:
            # Requisição para obter os nomes dos bancos
            response_bancos = requests.get(bancos_api_url)
            response_bancos.raise_for_status()
            bancos = response_bancos.json()
        except requests.exceptions.RequestException as e:
            error_message = f"Erro na requisição para API: {str(e)}"

        if op_numero:
            api_url = f'https://sua-api-aki/acompanhar_op?op={op_numero}&banco={banco_selecionado}'

            try:
                response = requests.get(api_url)
                data = response.json()

                # Depuração: Imprime o conteúdo retornado pela API
                print("Resposta da API:", data)

                if isinstance(data, list) and len(data) == 2:
                    op_info = data[0]  # Primeira lista com informações das notas fiscais
                    quantidade_entrada_item = data[1]  # Segunda lista com informações de quantidade

                    # Verificar a presença dos CFOPs
                    cfop_groups = {}
                    for item in op_info:
                        if 'ni_cfop' in item:
                            cfop_code = item['ni_cfop']
                            if cfop_code == '5902':
                                cfop_5902 = True
                            if cfop_code == '5124':
                                cfop_5124 = True
                            if cfop_code not in cfop_groups:
                                cfop_groups[cfop_code] = []
                            cfop_groups[cfop_code].append(item)
                        else:
                            error_message = "Dados incompletos na resposta da API."


            except requests.exceptions.RequestException as e:
                error_message = f"Erro na requisição para API: {str(e)}"
            except (KeyError, ValueError) as e:
                error_message = f"Dados incompletos ou erro na resposta da API: {str(e)}"

        contexto = {
            'nomes_bancos': bancos,
            'op_info': op_info,
            'op_numero': op_numero,
            'error_message': error_message,
            'cfop_5902': cfop_5902,
            'cfop_5124': cfop_5124,
            'cfop_groups': cfop_groups,
            'quantidade_entrada_item': quantidade_entrada_item,
            'xml_available': xml_available,  # Adiciona a variável ao contexto
        }

        # Se não for retorno XML, renderiza o template HTML
        if not return_xml:
            return render(request, 'acompanhar_op.html', contexto)

    return render(request, 'acompanhar_op.html', contexto)

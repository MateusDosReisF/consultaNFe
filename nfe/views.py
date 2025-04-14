# views.py
from django.shortcuts import render, redirect,get_object_or_404
from .models import Empresa,Etiqueta
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import ConfiguracaoEmpresaForm,ConfiguracaoEtiquetaForm
from .models import NotaFiscal
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
import xml.etree.ElementTree as ET
from pynfe.processamento.comunicacao import ComunicacaoSefaz
from pynfe.utils.descompactar import DescompactaGzip
from pynfe.utils.flags import NAMESPACE_NFE
from datetime import datetime
import base64
from lxml import etree
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from pynfe.entidades.evento import EventoManifestacaoDest

class EmpresaListView(ListView):
    model = Empresa
    template_name = 'empresa_list.html'
    context_object_name = 'empresas'
    paginate_by = 10

    def get_paginate_by(self, queryset):
        return self.request.GET.get('per_page', self.paginate_by)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['per_page'] = self.get_paginate_by(self.get_queryset())
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        cnpj = self.request.GET.get('cnpj')
        if cnpj:
            queryset = queryset.filter(cnpj__icontains=cnpj)
        return queryset
    
class EmpresaCreateView(CreateView):
    model = Empresa
    template_name = 'empresa_create.html'
    form_class = ConfiguracaoEmpresaForm
    success_url = reverse_lazy('nfe:empresa_list')

class EmpresaDetailView(DetailView):
    model = Empresa
    template_name = 'empresa_detail.html'

class EmpresaUpdateView(UpdateView):
    model = Empresa
    template_name = 'empresa_update.html'
    form_class = ConfiguracaoEmpresaForm
    success_url = reverse_lazy('nfe:empresa_list')

class EmpresaDeleteView(DeleteView):
    model = Empresa
    template_name = 'empresa_delete.html'
    success_url = reverse_lazy('nfe:empresa_list')

def consulta_notas(request):
    if request.method == 'POST':
        empresa_id = request.POST.get('empresa_id')
        empresa = get_object_or_404(Empresa, id=empresa_id)
    else:
        empresa = Empresa.objects.first()  # Supondo que há apenas uma empresa configurada
        if not empresa:
            return redirect('configurar_empresa')  # Redireciona para configurar empresa se não estiver configurada

    add_local='media/' + empresa.local_certificado.name
 
    certificado = add_local
    senha = empresa.senha_certificado
    uf = 'es'  # Ou outra UF configurável
    homologacao = False  # Ou True para ambiente de homologação
    CPFCNPJ = empresa.cnpj
    NSU = 0
    CHAVE = ''

    con = ComunicacaoSefaz(uf, certificado, senha, homologacao)
    ultNSU = 0
    maxNSU = 0
    cStat = 0

    while True:
        xml = con.consulta_distribuicao(cnpj=CPFCNPJ, chave=CHAVE, nsu=NSU)
        NSU = str(NSU).zfill(15)
        print(f'Nova consulta a partir do NSU: {NSU}')

        resposta = etree.fromstring(xml.text.encode('utf-8'))
        ns = {'ns': NAMESPACE_NFE}
        
        contador_resposta = len(resposta.xpath('//ns:retDistDFeInt/ns:loteDistDFeInt/ns:docZip', namespaces=ns))
        print(f'Quantidade de NSUs na consulta atual: {contador_resposta}')
        
        cStat = resposta.xpath('//ns:retDistDFeInt/ns:cStat', namespaces=ns)[0].text
        print(f'cStat: {cStat}')
        
        xMotivo = resposta.xpath('//ns:retDistDFeInt/ns:xMotivo', namespaces=ns)[0].text
        print(f'xMotivo: {xMotivo}')    
        
        maxNSU = resposta.xpath('//ns:retDistDFeInt/ns:maxNSU', namespaces=ns)[0].text
        print(f'maxNSU: {maxNSU}')
        
        if (cStat == '138'):
            for contador_xml in range(contador_resposta):
                tipo_schema = resposta.xpath('//ns:retDistDFeInt/ns:loteDistDFeInt/ns:docZip/@schema', namespaces=ns)[contador_xml]
                numero_nsu = resposta.xpath('//ns:retDistDFeInt/ns:loteDistDFeInt/ns:docZip/@NSU', namespaces=ns)[contador_xml]
                
                if (tipo_schema == 'procNFe_v4.00.xsd'): 
                    zip_resposta = resposta.xpath('//ns:retDistDFeInt/ns:loteDistDFeInt/ns:docZip', namespaces=ns)[contador_xml].text
                    resposta_descompactado = DescompactaGzip.descompacta(zip_resposta)
                    texto_descompactado = etree.tostring(resposta_descompactado).decode('utf-8')
                    
                    xml_tree = etree.fromstring(texto_descompactado)
                    namespaces = {'ns': 'http://www.portalfiscal.inf.br/nfe'} 
                    status_nf = xml_tree.xpath('//ns:protNFe/ns:infProt/ns:cStat', namespaces=namespaces)
                    data_emissao = xml_tree.xpath('//ns:NFe/ns:infNFe/ns:ide/ns:dhEmi', namespaces=namespaces)
                    numero_nota = xml_tree.xpath('//ns:NFe/ns:infNFe/ns:ide/ns:nNF', namespaces=namespaces)
                    cnpj_emissor = xml_tree.xpath('//ns:NFe/ns:infNFe/ns:emit/ns:CNPJ', namespaces=namespaces)
                    nome_emissor = xml_tree.xpath('//ns:NFe/ns:infNFe/ns:emit/ns:xNome', namespaces=namespaces)
                    destinatarios = xml_tree.xpath('//ns:NFe/ns:infNFe/ns:dest/ns:xNome', namespaces=namespaces)
                    destinatario_cnpjs = xml_tree.xpath('//ns:NFe/ns:infNFe/ns:dest/ns:CNPJ', namespaces=namespaces)
                    valores = xml_tree.xpath('//ns:NFe/ns:infNFe/ns:total/ns:ICMSTot/ns:vNF', namespaces=namespaces)
                    chave = xml_tree.xpath('//ns:protNFe/ns:infProt/ns:chNFe', namespaces=namespaces)

                    # Extraindo os valores (com fallback para None, caso os valores estejam ausentes)
                    numero_nota = numero_nota[0].text if numero_nota else None
                    cnpj_emissor = cnpj_emissor[0].text if cnpj_emissor else None
                    nome_emissor = nome_emissor[0].text if nome_emissor else None
                    destinatario_nome = destinatarios[0].text if destinatarios else None
                    destinatario_cnpj = destinatario_cnpjs[0].text if destinatario_cnpjs else None
                    valor_total = valores[0].text if valores else '0.00'
                    chave_nfe = chave[0].text if chave else None

                    
                    if not NotaFiscal.objects.filter(nf=numero_nota, chaveNfe=chave_nfe).exists():
                            # Criando e salvando a nova nota fiscal se não existir
                            nota_fiscal = NotaFiscal(
                                numero=numero_nsu,
                                nf=numero_nota,
                                data=data_emissao[0].text,
                                status_nfe=status_nf[0].text,
                                emissor=nome_emissor,
                                emissor_cnpj=cnpj_emissor,
                                destinatario=destinatario_nome,
                                destinatario_cnpj=destinatario_cnpj,
                                valor_total=valor_total,
                                xml=texto_descompactado,
                                chaveNfe=chave_nfe,
                            )
                            nota_fiscal.save()
                    else:
                        print(f"Nota Fiscal com nf {numero_nota} e chaveNfe {chave_nfe} já existe. Não será adicionada.")
                
                # Lógica para resumo e manifestação do destinatário
                elif (tipo_schema == 'resNFe_v1.01.xsd'):
                    pass
            
            NSU = resposta.xpath('//ns:retDistDFeInt/ns:ultNSU', namespaces=ns)[0].text
            print(f'NSU: {NSU}')
            
        elif (cStat == '137'):
            print(f'Não há mais documentos a pesquisar')
            break
        else:
            print(f'Falha')
            break

    notas_fiscais = NotaFiscal.objects.all()
    return render(request, 'consultar_notas.html', {'notas_fiscais': notas_fiscais,'empresas': Empresa.objects.all(), 'empresa_selecionada': empresa})


def ManifestaNotas(request):
    if request.method == 'POST':
        empresa_id = request.POST.get('empresa_id')
        empresa = get_object_or_404(Empresa, id=empresa_id)
    else:
        empresa = Empresa.objects.first()  # Supondo que há apenas uma empresa configurada
        if not empresa:
            return redirect('configurar_empresa')  # Redireciona para configurar empresa se não estiver configurada

    add_local='media/' + empresa.local_certificado.name
 
    certificado = add_local
    senha = empresa.senha_certificado
    uf = 'es'  # Ou outra UF configurável
    homologacao = False  # Ou True para ambiente de homologação
    CPFCNPJ = empresa.cnpj
    






import xml.etree.ElementTree as ET
from datetime import datetime
import base64

from django.core.paginator import Paginator

def listar_xmls(request):
    empresa_cnpj = request.GET.get('empresa_cnpj')  # CNPJ da empresa
    numero_nf = request.GET.get('numero_nf')  # Número da nota fiscal para filtragem
    notas_fiscais = NotaFiscal.objects.all()
    etiquetas = Etiqueta.objects.all()

    # Filtrando por CNPJ do destinatário, se aplicável
    if empresa_cnpj:
        notas_fiscais = notas_fiscais.filter(destinatario_cnpj=empresa_cnpj)
    
    # Filtrando por número da nota fiscal, se aplicável
    if numero_nf:
        notas_fiscais = notas_fiscais.filter(nf=numero_nf)
    notas_fiscais = notas_fiscais.order_by('-data')

    empresas = Empresa.objects.all()

    # Paginação
    per_page = request.GET.get('per_page', 10)  # Itens por página, com default de 10
    paginator = Paginator(notas_fiscais, per_page)  # Paginando as notas
    page_number = request.GET.get('page')  # Obtendo o número da página
    page_obj = paginator.get_page(page_number)  # Cria o objeto da página

    # Codificando XML e ajustando informações adicionais
    for nota in page_obj:
        x = nota.xml
        nota.xml_base64 = base64.b64encode(nota.xml.encode()).decode('utf-8')
        root = ET.fromstring(x)
        ns = {'nfe': 'http://www.portalfiscal.inf.br/nfe'}
        
        # Encontrar elementos dentro de <ide>
        ide = root.find('.//nfe:ide', namespaces=ns)
        if ide is not None:
            numero_nota = ide.find('nfe:nNF', namespaces=ns).text
            data_nota = ide.find('nfe:dhEmi', namespaces=ns).text

            # Encontrar elementos dentro de <emit>
            emit = root.find('.//nfe:dest', namespaces=ns)
            emit_real = root.find('.//nfe:emit', namespaces=ns)
            nome_emissor = emit.find('nfe:xNome', namespaces=ns).text if emit is not None else "Nome não encontrado"
            nome_emissor_real = emit_real.find('nfe:CNPJ', namespaces=ns).text if emit_real is not None else "CNPJ não encontrado"

            # Formatando data
            data_datetime = datetime.fromisoformat(data_nota[:-6])
            data_formatada = data_datetime.strftime('%d/%m/%Y')
        else:
            numero_nota = "Número não encontrado"
            data_datetime = None
            data_formatada = "Data não encontrada"
            nome_emissor = "Nome não encontrado"

        # Adiciona as informações às notas já paginadas
        nota.numero = numero_nota
        nota.data_formatada = data_formatada
        nota.nome_emissor = nome_emissor
        nota.nome_emissor_real = nome_emissor_real

    # Passando informações para o template
    context = {
        'empresas': empresas,
        'nf_completa': page_obj,  # Usar as notas paginadas
        'notas': notas_fiscais,
        'etiquetas': etiquetas,
        'page_obj': page_obj,  # Passar o objeto da página para a paginação
        'per_page': per_page  # Passar o valor de per_page para o template
    }

    return render(request, 'listar_xmls.html', context)

def adicionar_etiqueta(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            nota_id = data.get('nota_id')
            etiqueta_id = data.get('etiqueta_id')

            nota = NotaFiscal.objects.get(id=nota_id)
            etiqueta = Etiqueta.objects.get(id=etiqueta_id)

            # Associa a etiqueta à nota fiscal
            nota.etiqueta = etiqueta
            nota.save()

            # Retorna a resposta JSON com as informações da etiqueta
            return JsonResponse({
                'status': 'success',
                'etiqueta': {
                    'descricao': etiqueta.descricao,
                    'cor': etiqueta.cor
                }
            })
        except NotaFiscal.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Nota Fiscal não encontrada.'}, status=404)
        except Etiqueta.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Etiqueta não encontrada.'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
    return JsonResponse({'status': 'error', 'message': 'Método não permitido.'}, status=405)

        # ETIQUETA

class EtiquetaListView(ListView):
    model = Etiqueta
    template_name = 'etiqueta_list.html'
    context_object_name = 'etiquetas'
    paginate_by = 10

    def get_paginate_by(self, queryset):
        # Override the paginate_by variable based on GET parameter
        return self.request.GET.get('per_page', self.paginate_by)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['per_page'] = self.get_paginate_by(self.get_queryset())
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

class EtiquetaCreateView(CreateView):
    model = Etiqueta
    template_name = 'etiqueta_create.html'
    form_class = ConfiguracaoEtiquetaForm
    success_url = reverse_lazy('nfe:etiqueta_list')

class EtiquetaUpdateView(UpdateView):
    model = Etiqueta
    template_name = 'etiqueta_update.html'
    form_class = ConfiguracaoEtiquetaForm
    success_url = reverse_lazy('nfe:etiqueta_list')

class EtiquetaDeleteView(DeleteView):
    model = Etiqueta
    template_name = 'etiqueta_delete.html'
    success_url = reverse_lazy('nfe:etiqueta_list')
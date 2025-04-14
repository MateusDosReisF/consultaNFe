from django import template
import locale


# Registra o filtro no template engine Django
register = template.Library()

@register.filter
def formatar_valor_brasileiro(valor):
    try:
        # Converta o valor para float, se possível
        valor_float = float(valor)
    except (ValueError, TypeError):
        # Se não for possível converter, retorne o valor original ou uma string de erro
        return valor
    
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
    return locale.format_string('%.2f', valor_float, grouping=True)



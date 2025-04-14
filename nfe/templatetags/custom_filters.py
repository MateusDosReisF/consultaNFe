from django import template
import locale
import sys

# Registra o filtro no template engine Django
register = template.Library()

@register.filter
def formatar_valor_brasileiro(valor):
    try:
        # Converte o valor para float, se possível
        valor_float = float(valor)
    except (ValueError, TypeError):
        # Se não for possível converter, retorna o valor original ou uma string de erro
        return valor

    # Ajusta a localidade dependendo do sistema operacional
    try:
        if sys.platform == "win32":
            # Localidade para Windows em inglês
            locale.setlocale(locale.LC_ALL, 'Portuguese_Brazil.1252')
        else:
            # Localidade para sistemas baseados em Unix
            locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
    except locale.Error:
        return valor  # Se a localidade não for suportada, retorna o valor sem formatação

    # Formata o valor como moeda brasileira
    return locale.format_string('%.2f', valor_float, grouping=True)

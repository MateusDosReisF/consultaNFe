from django import template
from datetime import datetime

register = template.Library()

@register.filter
def formatar_data_brasileira(data_iso):
    try:
        # Converte a string ISO 8601 em um objeto datetime
        data_obj = datetime.fromisoformat(data_iso)
        # Formata a data no formato brasileiro
        return data_obj.strftime('%d/%m/%Y %H:%M:%S')
    except (ValueError, TypeError):
        # Retorna o valor original se houver um erro
        return data_iso

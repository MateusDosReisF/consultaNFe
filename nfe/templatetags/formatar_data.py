from django import template
from datetime import datetime

register = template.Library()

@register.filter
def formatar_data_brasileira(data_iso):
    try:
        data_obj = datetime.fromisoformat(data_iso)
        return data_obj.strftime('%d/%m/%Y')
    except (ValueError, TypeError):
        return data_iso

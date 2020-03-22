from django import template
register = template.Library()
@register.filter
def get_type(value):
    if value<75:
        return True
    else:
        return False    


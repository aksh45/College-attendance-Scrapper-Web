from django import template
register = template.Library()
@register.filter
def get_type(value):
    if type(value)==float and value<75:
        return "red"
    elif type(value)==float and value>75:
        return "#006400"
    else:
        return False    


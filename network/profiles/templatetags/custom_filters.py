from django import template

register = template.Library()


@register.filter
def round_to(value, decimals):
    try:
        return f"{float(value):.{decimals}f}"
    except (ValueError, TypeError):
        return value

from django import template

register = template.Library()


@register.filter
def until(value):
    """Returns a range up to the given value."""
    try:
        return range(int(value))
    except (ValueError, TypeError):
        return range(0)


@register.filter
def subtract(value, arg):
    """Subtracts arg from value."""
    try:
        return int(value) - int(arg)
    except (ValueError, TypeError):
        return value
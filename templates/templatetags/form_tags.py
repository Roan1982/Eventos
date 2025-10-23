from django import template
from django.utils.html import format_html

register = template.Library()


@register.filter(name='add_class')
def add_class(field, css):
    """Add CSS class(es) to a form field's widget rendering.

    Usage: {{ form.field|add_class:'form-control' }}
    """
    try:
        existing = field.field.widget.attrs.get('class', '')
        classes = (existing + ' ' + css).strip()
        return field.as_widget(attrs={'class': classes})
    except Exception:
        return field

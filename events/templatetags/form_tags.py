from django import template

register = template.Library()


@register.filter(name='add_class')
def add_class(field, css):
    try:
        existing = field.field.widget.attrs.get('class', '')
        classes = (existing + ' ' + css).strip()
        return field.as_widget(attrs={'class': classes})
    except Exception:
        return field

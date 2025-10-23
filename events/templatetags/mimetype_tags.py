from django import template

register = template.Library()


@register.filter
def mimetype_startswith(content_type, prefix):
    """Return True if content_type starts with prefix (safe in templates)."""
    try:
        return str(content_type).startswith(prefix)
    except Exception:
        return False

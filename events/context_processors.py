from .models import Notification

def unread_notifications_count(request):
    """Context processor that adds the number of unread notifications for the logged user."""
    if not request.user.is_authenticated:
        return {}
    try:
        count = Notification.objects.filter(user=request.user, is_read=False).count()
    except Exception:
        # In case DB is not available in some contexts (tests/startup), fail silently
        count = 0
    return {'unread_notifications_count': count}

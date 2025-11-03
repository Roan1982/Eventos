from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.conf import settings
from django.urls import reverse

from .models import Event, UserInterest, Notification

@receiver(pre_save, sender=Event)
def capture_previous_status(sender, instance, **kwargs):
    """Store previous status on instance to detect transitions on post_save."""
    if not instance.pk:
        instance._previous_status = None
        return
    try:
        prev = Event.objects.get(pk=instance.pk)
        instance._previous_status = prev.status
    except Event.DoesNotExist:
        instance._previous_status = None


@receiver(post_save, sender=Event)
def notify_on_event_change(sender, instance, created, **kwargs):
    """Create Notification rows for users whose interests match this event.

    We only create notifications for:
    - newly created events with status 'published'
    - events that changed status to 'published'
    - updates to already published events (as 'event_update')
    """
    # Helper to create notification for a user
    def _create_notification_for(user, ntype, title, message):
        # Avoid notifying the event creator about their own actions
        if user == instance.creator:
            return
        Notification.objects.create(
            user=user,
            event=instance,
            notification_type=ntype,
            title=title,
            message=message[:1000]
        )

    # Determine event action
    prev_status = getattr(instance, '_previous_status', None)

    # New publish
    if created and instance.status == 'published':
        ntype = 'new_event'
    # Status changed to published
    elif not created and instance.status == 'published' and prev_status != 'published':
        ntype = 'new_event'
    # Update to an already published event
    elif not created and instance.status == 'published' and prev_status == 'published':
        ntype = 'event_update'
    else:
        # No notification needed (e.g., draft, cancelled without publish)
        return

    # Find users interested in this category and opted-in
    interests = UserInterest.objects.filter(categories=instance.category, notify_new_events=True).select_related('user')

    title = instance.title if ntype == 'new_event' else f'Actualizado: {instance.title}'
    message = instance.description or ''

    for ui in interests:
        _create_notification_for(ui.user, ntype, title, message)

from celery import shared_task
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.utils import timezone
from django.conf import settings
from django.urls import reverse

from .models import Notification

@shared_task
def send_notification_digests():
    """Send one aggregated email per user containing all pending notifications.

    This task looks for Notification objects with email_sent=False, groups
    them by user, renders a single email per user containing the list of
    notifications, sends it, and marks those notifications email_sent=True.
    """
    now = timezone.now()
    qs = Notification.objects.filter(email_sent=False).select_related('user', 'event')
    users = {}
    for n in qs:
        users.setdefault(n.user_id, []).append(n)

    for user_id, notifs in users.items():
        user = notifs[0].user
        # Render email template
        context = {
            'user': user,
            'notifications': notifs,
            'site_name': getattr(settings, 'DOMAIN', ''),
            'site_url': getattr(settings, 'SITE_URL', ''),
        }
        subject = f'Notificaciones de {len(notifs)} elemento(s) en {context["site_name"] or "tu sitio"}'
        text_body = render_to_string('emails/notification_digest.txt', context)
        html_body = render_to_string('emails/notification_digest.html', context)

        msg = EmailMultiAlternatives(subject, text_body, settings.DEFAULT_FROM_EMAIL, [user.email])
        msg.attach_alternative(html_body, 'text/html')
        try:
            msg.send()
            # Mark notifications as emailed
            Notification.objects.filter(id__in=[n.id for n in notifs]).update(email_sent=True)
        except Exception:
            # If sending fails, skip marking so it'll be retried next run
            continue

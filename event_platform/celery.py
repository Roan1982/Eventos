import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'event_platform.settings')

app = Celery('event_platform')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# Example schedule for periodic digest (every 15 minutes)
app.conf.beat_schedule = {
    'send-notification-digests-every-15-minutes': {
        'task': 'events.tasks.send_notification_digests',
        'schedule': 60 * 15,
    },
}

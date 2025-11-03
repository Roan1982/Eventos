import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'event_platform.settings')
import django
django.setup()

from django.contrib.auth.models import User
from events.models import Notification

print('Users:', list(User.objects.values_list('username', flat=True)))
print('Notifications count:', Notification.objects.count())
for n in Notification.objects.all()[:20]:
    print(n.pk, n.user.username, n.notification_type, n.email_sent)

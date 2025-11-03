#!/usr/bin/env python
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE','event_platform.settings')
django.setup()
from events.models import Notification, UserInterest
from django.db.models import Count
print('INTERESTS', UserInterest.objects.count())
print('NOTIFICATIONS_TOTAL', Notification.objects.count())
print('NOTIFICATIONS_SENT', Notification.objects.filter(email_sent=True).count())
print('NOTIFICATIONS_UNREAD', Notification.objects.filter(is_read=False).count())
for row in Notification.objects.values('user__username').annotate(total=Count('id')).order_by('-total'):
    print('BY_USER', row)

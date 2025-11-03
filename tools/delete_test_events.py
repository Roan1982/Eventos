#!/usr/bin/env python3
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','event_platform.settings')
import django
django.setup()
from events.models import Event, Notification
from django.contrib.auth import get_user_model
User = get_user_model()

qs1 = Event.objects.filter(creator__username='cmdtester')
qs2 = Event.objects.filter(title__icontains='Cmd Event')
qs3 = Event.objects.filter(slug__startswith='cmd-event')
qs = (qs1 | qs2 | qs3).distinct()
items = list(qs.values('id','title','slug','creator__username'))
print('FOUND:', items)
ids = [i['id'] for i in items]
if not ids:
    print('No test events found; nothing to delete.')
else:
    # Delete related notifications first
    notifs_deleted, _ = Notification.objects.filter(event__id__in=ids).delete()
    events_deleted, _ = Event.objects.filter(id__in=ids).delete()
    print(f'Deleted notifications count (cascade result): {notifs_deleted}')
    print(f'Deleted events count (cascade result): {events_deleted}')
    # final check
    remaining = list(Event.objects.filter(id__in=ids).values('id'))
    print('Remaining event ids (should be empty):', remaining)

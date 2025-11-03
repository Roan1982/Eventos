import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'event_platform.settings')
import django
django.setup()
from django.test import Client
from django.contrib.auth import get_user_model
User = get_user_model()

# Ensure a test user exists
u, created = User.objects.get_or_create(username='debugtester', defaults={'email':'debug@test.local'})
if created:
    u.set_password('testpass')
    u.save()

c = Client()
logged = c.login(username='debugtester', password='testpass')
print('logged in:', logged)
resp = c.get('/eventos/notificaciones/')
print('status_code:', resp.status_code)
print('content_snippet:', resp.content.decode('utf-8')[:400])

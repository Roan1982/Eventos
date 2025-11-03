import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'event_platform.settings')
import django
django.setup()

from django.test import Client
from django.contrib.auth.models import User

c = Client()
# Use HTTPS in the test client so the app doesn't redirect to HTTPS and drop POST data
c.defaults['wsgi.url_scheme'] = 'https'
resp = c.post('/accounts/signup/', {
    'username': 'alice',
    'email': 'alice@example.com',
    'password1': 'ASecurePass123',
    'password2': 'ASecurePass123'
}, HTTP_X_FORWARDED_PROTO='https')
print('STATUS:', resp.status_code)
print('HEADERS:', dict(resp.items()))
print('CONTENT:\n', resp.content.decode('utf-8'))
print('USERS ALICE:', User.objects.filter(username='alice').count())
print('ALL USERS:', list(User.objects.values_list('username', flat=True)))

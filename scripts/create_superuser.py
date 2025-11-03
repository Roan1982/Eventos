from django.contrib.auth import get_user_model
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'event_platform.settings')
import django
django.setup()
User = get_user_model()
username = 'admin'
email = 'roaniamusic@gmail.com'
password = 'Angelito1982'
if User.objects.filter(username=username).exists():
    print('superuser exists')
else:
    User.objects.create_superuser(username=username, email=email, password=password)
    print('superuser created')

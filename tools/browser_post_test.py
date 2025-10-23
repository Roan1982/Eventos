from django.contrib.auth import get_user_model
from django.test import Client
from django.core.files.uploadedfile import SimpleUploadedFile
from events.models import Category

def run():
    User = get_user_model()
    user, _ = User.objects.get_or_create(username='browser_tester', defaults={'email':'b@test'})
    user.set_password('test')
    user.save()
    cat, _ = Category.objects.get_or_create(name='WebCat')

    c = Client()
    logged = c.login(username='browser_tester', password='test')
    print('logged in?', logged)

    f = SimpleUploadedFile('tiny.png', b'\x89PNG\r\n\x1a\n', content_type='image/png')
    post = {
        'title': 'Web Event',
        'description': 'From test client',
        'category': str(cat.id),
        'start_date': '2025-10-25',
        'start_time': '09:00',
        'end_date': '2025-10-25',
        'end_time': '11:00',
        'price': '0',
        'venue_name': 'Web Hall',
        'address': '123 Web St',
        'city': 'WebCity',
        'capacity': '30',
        'status': 'published',
    }

    resp = c.post('/eventos/crear/', post, follow=True, files={'media_files': f})
    print('status code', resp.status_code)
    print('redirect chain', resp.redirect_chain)
    content = resp.content.decode('utf-8')
    if 'Errores en el formulario' in content:
        idx = content.find('Errores en el formulario')
        print(content[idx:idx+800])
    else:
        print('No inline error block found in response; printing first 800 chars:')
        print(content[:800])

if __name__ == '__main__':
    run()

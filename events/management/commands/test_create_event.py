from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils.datastructures import MultiValueDict
from django.core.files.uploadedfile import SimpleUploadedFile

from events.forms import EventForm
from events.models import Category, Event


class Command(BaseCommand):
    help = 'Create a test event using EventForm to validate save and media handling'

    def handle(self, *args, **options):
        User = get_user_model()
        user, created = User.objects.get_or_create(username='cmdtester', defaults={'email':'cmd@test.local'})
        if created:
            user.set_password('testpass')
            user.save()

        cat, _ = Category.objects.get_or_create(name='CmdCat')

        data = {
            'title': 'Cmd Event',
            'description': 'Created by management command',
            'category': str(cat.id),
            'start_date': '2025-10-24',
            'start_time': '10:00',
            'end_date': '2025-10-24',
            'end_time': '12:00',
            'price': '0',
            'venue_name': 'CLI Hall',
            'address': '123 CLI St',
            'city': 'Local',
            'capacity': '50',
            'status': 'published',
        }

        # Build a SimpleUploadedFile and post it directly to EventForm to test
        # server-side handling (avoids test client multipart quirks here).
        f = SimpleUploadedFile('tiny.png', b'\x89PNG\r\n\x1a\n', content_type='image/png')
        from django.utils.datastructures import MultiValueDict
        files = MultiValueDict()
        files.setlist('media_files', [f])

        form = EventForm(data, files=files)
        # attach the creator before saving so metadata is correct
        form.instance.creator = user
        if form.is_valid():
            ev = form.save()
            print('Form saved event id', ev.id)
            print('media count', ev.media.count())
        else:
            print('Form errors', form.errors)

def run():
    from django.contrib.auth import get_user_model
    from django.utils.datastructures import MultiValueDict
    from django.core.files.uploadedfile import SimpleUploadedFile
    from events.forms import EventForm
    from events.models import Category, MediaBlob

    User = get_user_model()
    user, _ = User.objects.get_or_create(username='filetester', defaults={'email':'f@test'})
    user.set_password('test')
    user.save()
    cat, _ = Category.objects.get_or_create(name='FileTestCat')

    data = {
        'title': 'FileTest',
        'description': 'File test',
        'category': str(cat.id),
        'start_date': '2025-12-01',
        'start_time': '09:00',
        'end_date': '2025-12-01',
        'end_time': '10:00',
        'price': '0',
        'venue_name': 'V',
        'address': 'A',
        'city': 'C',
        'capacity': '10',
        'status': 'published',
    }

    f = SimpleUploadedFile('one.png', b'\x89PNG\r\n\x1a\n', content_type='image/png')
    # test with key 'media_files'
    files = MultiValueDict()
    files.setlist('media_files', [f])
    form = EventForm(data, files=files)
    form.instance.creator = user
    if form.is_valid():
        ev = form.save()
        print('media_files key: created', ev.media.count())
    else:
        print('media_files key: errors', form.errors)

    # test with key 'media_files[]'
    f2 = SimpleUploadedFile('two.png', b'\x89PNG\r\n\x1a\n', content_type='image/png')
    files2 = MultiValueDict()
    files2.setlist('media_files[]', [f2])
    form2 = EventForm(data, files=files2)
    form2.instance.creator = user
    if form2.is_valid():
        ev2 = form2.save()
        print('media_files[] key: created', ev2.media.count())
    else:
        print('media_files[] key: errors', form2.errors)

if __name__ == '__main__':
    run()

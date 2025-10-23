def run():
    from django.contrib.auth import get_user_model
    from events.models import Event, Category
    from events.forms import EventForm
    import datetime

    User = get_user_model()
    user = User.objects.first()
    cat, _ = Category.objects.get_or_create(name='EditTestCat')
    ev = Event.objects.create(
        creator=user,
        title='Existing',
        description='Existing',
        category=cat,
        start_datetime=datetime.datetime(2025,10,30,9,30),
        end_datetime=datetime.datetime(2025,10,30,11,0),
        price=0, venue_name='V', address='A', city='C', capacity=10, status='published', slug='existing-test'
    )
    form = EventForm(instance=ev)
    print('initial start_date', form.initial.get('start_date'))
    print('initial start_time', form.initial.get('start_time'))
    print('initial end_date', form.initial.get('end_date'))
    print('initial end_time', form.initial.get('end_time'))

if __name__ == '__main__':
    run()

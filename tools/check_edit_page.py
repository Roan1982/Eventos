def run():
    from django.test import Client
    from django.contrib.auth import get_user_model
    from events.models import Event, Category
    import datetime

    User = get_user_model()
    user, _ = User.objects.get_or_create(username='edit_page_tester', defaults={'email':'ep@test'})
    user.set_password('test')
    user.save()

    cat, _ = Category.objects.get_or_create(name='EditPageCat')
    ev = Event.objects.create(
        creator=user,
        title='ToEdit',
        description='For edit page',
        category=cat,
        start_datetime=datetime.datetime(2025,11,5,8,15),
        end_datetime=datetime.datetime(2025,11,5,10,45),
        price=0, venue_name='V', address='A', city='C', capacity=20, status='published', slug='to-edit'
    )

    c = Client()
    logged = c.login(username='edit_page_tester', password='test')
    print('logged?', logged)
    resp = c.get(f'/eventos/{ev.slug}/editar/')
    html = resp.content.decode('utf-8')
    # find input tags for start_date, start_time, end_date, end_time
    for idname in ('id_start_date','id_start_time','id_end_date','id_end_time'):
        idx = html.find(f'id="{idname}"')
        if idx == -1:
            print(idname, 'NOT FOUND')
        else:
            snippet = html[idx:idx+200]
            # try to show the enclosing <input...>
            start = html.rfind('<',0,idx)
            end = html.find('>', idx)
            print(idname, html[start:end+1])

if __name__ == '__main__':
    run()

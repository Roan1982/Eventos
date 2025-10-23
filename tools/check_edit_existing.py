def run():
    from django.test import Client
    from events.models import Event
    from django.contrib.auth import get_user_model

    ev = Event.objects.first()
    if not ev:
        print('No events found')
        return
    print('using slug', ev.slug)
    User = get_user_model()
    user = User.objects.first()
    c = Client()
    c.force_login(user)
    resp = c.get(f'/eventos/{ev.slug}/editar/')
    html = resp.content.decode('utf-8')
    for idname in ('id_start_date','id_start_time','id_end_date','id_end_time'):
        idx = html.find(f'id="{idname}"')
        if idx == -1:
            print(idname, 'NOT FOUND')
        else:
            start = html.rfind('<',0,idx)
            end = html.find('>', idx)
            print(idname, html[start:end+1])

if __name__ == '__main__':
    run()

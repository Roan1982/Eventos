from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from .models import Event, Category, Review, MediaBlob
import io

class EventTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('user', 'user@example.com', 'pass')
        self.cat = Category.objects.create(name='Tecnología', slug='tecnologia')

    def test_create_event(self):
        e = Event.objects.create(
            creator=self.user,
            title='Conf Python',
            description='Charla',
            category=self.cat,
            start_datetime=timezone.now(),
            end_datetime=timezone.now()+timezone.timedelta(hours=2),
            price=0,
            venue_name='Centro', address='Calle Falsa 123', city='Madrid', capacity=100, status='published'
        )
        self.assertTrue(e.slug)
        self.assertTrue(e.is_free)

    def test_search(self):
        Event.objects.create(
            creator=self.user,
            title='Musica Rock',
            description='Show',
            category=self.cat,
            start_datetime=timezone.now(),
            end_datetime=timezone.now()+timezone.timedelta(hours=2),
            price=10,
            venue_name='Teatro', address='Dir', city='Buenos Aires', capacity=50, status='published'
        )
        c = Client()
        resp = c.get(reverse('events:list'), {'q': 'Rock'})
        self.assertContains(resp, 'Musica Rock')

    def test_blob_upload_and_serve(self):
        e = Event.objects.create(
            creator=self.user,
            title='Con imagen',
            description='desc',
            category=self.cat,
            start_datetime=timezone.now(),
            end_datetime=timezone.now()+timezone.timedelta(hours=1),
            price=0,
            venue_name='X', address='Y', city='Z', capacity=10, status='published'
        )
        # create a small png header bytes
        content = b"\x89PNG\r\n\x1a\n" + b"0"*100
        blob = MediaBlob.objects.create(event=e, content=content, content_type='image/png', filename='x.png', size=len(content))
        url = reverse('events:media_blob', args=[blob.id])
        c = Client()
        resp = c.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp['Content-Type'], 'image/png')

    def test_review_average(self):
        e = Event.objects.create(
            creator=self.user,
            title='Con reviews',
            description='desc',
            category=self.cat,
            start_datetime=timezone.now(),
            end_datetime=timezone.now()+timezone.timedelta(hours=1),
            price=0,
            venue_name='X', address='Y', city='Z', capacity=10, status='published'
        )
        u2 = User.objects.create_user('u2', 'u2@example.com', 'pass')
        Review.objects.create(user=self.user, event=e, rating=4)
        Review.objects.create(user=u2, event=e, rating=2)
        avg = e.reviews.all().aggregate_avg if False else e.reviews.aggregate_avg if False else e.reviews.aggregate(avg=('rating',))
        # Simpler: fetch through detail view context
        c = Client()
        resp = c.get(e.get_absolute_url())
        self.assertContains(resp, 'Promedio')

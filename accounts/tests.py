from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

class AccountsTests(TestCase):
    def test_signup_and_verify_flow(self):
        c = Client()
        resp = c.post(reverse('accounts:signup'), {
            'username': 'alice', 'email': 'alice@example.com',
            'password1': 'ASecurePass123', 'password2': 'ASecurePass123'
        })
        # Should redirect to login
        self.assertEqual(resp.status_code, 302)

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator as token_generator

class AccountsTests(TestCase):
    def test_signup_and_verify_flow(self):
        c = Client()
        # Ensure test client uses HTTPS so middleware (SECURE_SSL_REDIRECT) doesn't force a redirect
        c.defaults['wsgi.url_scheme'] = 'https'

        resp = c.post(reverse('accounts:signup'), {
            'username': 'alice', 'email': 'alice@example.com',
            'password1': 'ASecurePass123', 'password2': 'ASecurePass123'
        }, HTTP_X_FORWARDED_PROTO='https')
        # Should redirect to login (301 or 302 depending on middleware)
        self.assertIn(resp.status_code, (301, 302))
        # User should be created but inactive until email verification
        user = User.objects.get(username='alice')
        self.assertFalse(user.is_active)

        # Login should be rejected for inactive users
        logged = c.login(username='alice', password='ASecurePass123')
        self.assertFalse(logged)

        # Now simulate clicking the verification link
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = token_generator.make_token(user)
        verify_url = reverse('accounts:verify_email', args=[uid, token])
        resp = c.get(verify_url)
        # verify view performs a redirect; accept 301/302 (tests run under different middleware settings)
        self.assertIn(resp.status_code, (301, 302))

        # Refresh from DB and assert user is active
        user.refresh_from_db()
        self.assertTrue(user.is_active)

        # Now login should succeed
        logged = c.login(username='alice', password='ASecurePass123')
        self.assertTrue(logged)

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

User = get_user_model()


class RegisterViewTests(TestCase):
    def test_get_renders_form(self):
        resp = self.client.get(reverse('register'))
        self.assertEqual(resp.status_code, 200)

    def test_register_creates_user_and_logs_in(self):
        resp = self.client.post(
            reverse('register'),
            {
                'username': 'newcook',
                'email': 'new@example.com',
                'password1': 'a-strong-pw-9876',
                'password2': 'a-strong-pw-9876',
            },
        )
        self.assertRedirects(resp, reverse('cookbook:recipe_list'))
        user = User.objects.get(username='newcook')
        self.assertEqual(user.email, 'new@example.com')
        # form_valid logs the new user in.
        self.assertEqual(int(self.client.session['_auth_user_id']), user.pk)

    def test_password_mismatch_rerenders_without_creating(self):
        resp = self.client.post(
            reverse('register'),
            {
                'username': 'nope',
                'email': 'nope@example.com',
                'password1': 'a-strong-pw-9876',
                'password2': 'different-pw-1234',
            },
        )
        self.assertEqual(resp.status_code, 200)
        self.assertFalse(User.objects.filter(username='nope').exists())


class LoginLogoutTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='member', password='pw-verylong-123'
        )

    def test_login_page_renders(self):
        self.assertEqual(self.client.get(reverse('login')).status_code, 200)

    def test_login_succeeds(self):
        resp = self.client.post(
            reverse('login'),
            {'username': 'member', 'password': 'pw-verylong-123'},
        )
        self.assertEqual(resp.status_code, 302)
        self.assertIn('_auth_user_id', self.client.session)

    def test_logout_redirects(self):
        self.client.force_login(self.user)
        resp = self.client.post(reverse('logout'))
        self.assertEqual(resp.status_code, 302)


class UserModelTests(TestCase):
    def test_custom_user_model_is_active(self):
        user = User.objects.create_user(username='u', password='pw-verylong-123')
        self.assertTrue(user.is_active)
        self.assertEqual(str(user), 'u')

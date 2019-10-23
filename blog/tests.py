from django.test import TestCase, SimpleTestCase
from django.urls import reverse

from django.contrib.auth import get_user_model
from django.contrib.auth.models import User


class HomeAndAbout(TestCase):
    def test_home_status_code(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)

    def test_home_name_status_code(self):
        resp = self.client.get(reverse('home'))
        self.assertEqual(resp.status_code, 200)

    def test_home_template(self):
        resp = self.client.get('/')
        self.assertTemplateUsed(resp, 'blog/home.html')

    def test_about_status_code(self):
        resp = self.client.get('/about/')
        self.assertEqual(resp.status_code, 200)

    def test_about_name_status_code(self):
        resp = self.client.get(reverse('about'))
        self.assertEqual(resp.status_code, 200)

    def test_about_template(self):
        resp = self.client.get('/about/')
        self.assertTemplateUsed(resp, 'blog/about.html')


class Authentication(TestCase):
    def setUp(self):
        test_user = get_user_model().objects.create_user(
            username="testing_user",
            email="testing@mail.com",
            password="testing_password"
        )

        login = self.client.login(
            username='testing_user',
            password='testing_password'
        )

    def test_login_status_code(self):
        resp = self.client.get('/login/')
        self.assertEqual(resp.status_code, 200)

    def test_login_name_status_code(self):
        resp = self.client.get(reverse('login'))
        self.assertEqual(resp.status_code, 200)

    def test_login_template(self):
        resp = self.client.get('/login/')
        self.assertTemplateUsed(resp, 'users/login.html')

    def test_reset_password_status_code(self):
        resp = self.client.get('/password-reset/')
        self.assertEqual(resp.status_code, 200)

    def test_reset_password_name_status_code(self):
        resp = self.client.get(reverse('password_reset'))
        self.assertEqual(resp.status_code, 200)

    def test_change_password_status_code(self):
        resp = self.client.get('/password-change/')
        self.assertEqual(resp.status_code, 200)

    def test_change_password_name_status_code(self):
        resp = self.client.get(reverse('password_change'))

    def test_change_password_template(self):
        resp = self.client.get('/password-change/')
        self.assertTemplateUsed(resp, 'users/password_change.html')

    def test_change_password_modification(self):
        resp = self.client.post(reverse('password_change'), {
            'old_password': 'testing_password',
            'new_password1': 'new_secret_key',
            'new_password2': 'new_secret_key'
        })

        self.assertEqual(resp.status_code, 302)
        self.client.get('/logout/')
        # Login with the new credentials
        login = self.client.post(
            '/login/',
            {'username': 'testing_user', 'password': 'new_secret_key'},
            follow=True)
        self.assertTrue(login.context['user'].is_active)
        self.client.get('/logout/')
        # Login with the old/wrong credentials
        login = self.client.post(
            '/login/',
            {'username': 'testing_user', 'password': 'testing_password'},
            follow=True)
        self.assertFalse(login.context['user'].is_active)


class SignUp(TestCase):

    def test_sign_up_status_code(self):
        resp = self.client.get('/signup/')
        self.assertEqual(resp.status_code, 200)

    def test_sign_up_name_status_code(self):
        resp = self.client.get(reverse('signup'))
        self.assertEqual(resp.status_code, 200)

    def test_sign_up_template(self):
        resp = self.client.get('/signup/')
        self.assertTemplateUsed(resp, 'users/signup.html')

    def test_sign_up_post(self):
        new_user = get_user_model().objects.create_user(
            "testing_user",
            "testing@mail.com")

        self.assertEqual(get_user_model().objects.all().count(), 1)
        self.assertEqual(get_user_model().objects.all()
                         [0].username, "testing_user")
        self.assertEqual(get_user_model().objects.all()
                         [0].email, "testing@mail.com")

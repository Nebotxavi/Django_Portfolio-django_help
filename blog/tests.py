from django.test import TestCase, SimpleTestCase
from django.urls import reverse

from selenium import webdriver

from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

from .models import Post


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


class CRUD(TestCase):
    def setUp(self):
        self.test_user = get_user_model().objects.create_user(
            username="testing_user",
            email="testing@mail.com",
            password="testing_password"
        )

        login = self.client.login(
            username='testing_user',
            password='testing_password'
        )

        self.test_post = Post.objects.create(
            title="testing title",
            content="testing content",
            author=self.test_user
        )

    # Read
    def test_detail_content(self):
        resp = self.client.get(reverse('post_detail', args='1'))
        self.assertContains(resp, 'testing title')
        self.assertContains(resp, 'testing content')
        self.assertContains(resp, 'testing_user')
        self.assertEqual(resp.status_code, 200)

    def test_detail_post_status_code(self):
        resp = self.client.get('/post/1/')
        self.assertEqual(resp.status_code, 200)

    def test_detail_post_template(self):
        resp = self.client.get(reverse('post_detail', args='1'))
        self.assertTemplateUsed(resp, 'blog/post_detail.html')

    # Create

    def test_new_post_status_code(self):
        resp = self.client.get('/post/new_post/')
        self.assertEqual(resp.status_code, 200)

    def test_new_post_name_status_code(self):
        resp = self.client.get(reverse('post_create'))
        self.assertEqual(resp.status_code, 200)

    def test_new_post_template_status_code(self):
        resp = self.client.get('/post/new_post/')
        self.assertTemplateUsed(resp, 'blog/post_form.html')

    def test_new_post_create(self):
        resp = self.client.post('/post/new_post/', {
            'title': 'testing title 2',
            'content': 'testing content 2',
        })

        self.assertEqual(resp.status_code, 302)

        resp = self.client.get(reverse('post_detail', args='2'))
        self.assertContains(resp, 'testing title 2')
        self.assertContains(resp, 'testing content 2')
        self.assertContains(resp, 'testing_user')
        self.assertNotContains(resp, 'testing title 1')

    # Update

    def test_update_post_status_code(self):
        resp = self.client.get('/post/1/update/')
        self.assertEqual(resp.status_code, 200)

    def test_update_post_name_status_code(self):
        resp = self.client.get(reverse('post_update', args='1'))
        self.assertEqual(resp.status_code, 200)

    def test_update_post_template(self):
        resp = self.client.get('/post/1/update/')
        self.assertTemplateUsed(resp, 'blog/post_form.html')

    def test_update_post_update(self):
        resp = self.client.post('/post/1/update/', {
            'title': 'testing title updated',
            'content': 'testing content updated',
            'tags': 'new testing tag'
        })

        self.assertEqual(resp.status_code, 302)

        resp = self.client.get(reverse('post_detail', args='1'))
        self.assertContains(resp, 'testing title updated')
        self.assertContains(resp, 'testing content updated')
        self.assertContains(resp, 'testing_user')
        self.assertNotContains(resp, 'testing title 1')

    # Remove

    def test_delete_post_status_code(self):
        resp = self.client.get('/post/1/delete/')
        self.assertEqual(resp.status_code, 200)

    def test_delete_post_name_status_code(self):
        resp = self.client.get(reverse('post_delete', args='1'))
        self.assertEqual(resp.status_code, 200)

    def test_delete_post_template(self):
        resp = self.client.get('/post/1/delete/')
        self.assertTemplateUsed(resp, 'blog/post_confirm_delete.html')

    def test_delete_post_delete(self):
        resp = self.client.post('/post/1/delete/')
        self.assertEqual(Post.objects.all().count(), 0)


class Tags(TestCase):
    def setUp(self):
        self.test_user = get_user_model().objects.create_user(
            username="testing_user",
            email="testing@mail.com",
            password="testing_password"
        )

        self.test_post = Post.objects.create(
            title="testing title",
            content="testing content",
            author=self.test_user
        )

        self.test_post.tags.add("testing_tag", "second tag")

    def test_tags_in_DB(self):
        self.assertEqual(Post.tags.all().count(), 2)
        self.assertEqual(Post.tags.get(name='testing_tag').name, 'testing_tag')
        self.assertEqual(Post.tags.get(name='second tag').name, 'second tag')

    def test_tags_in_post_detail(self):
        resp = self.client.get('/post/1/')
        self.assertContains(resp, 'testing_tag')
        self.assertContains(resp, 'second tag')


class UserPostsList(TestCase):
    def setUp(self):
        self.test_user = get_user_model().objects.create_user(
            username="testing_user_1",
            email="testing1@mail.com",
            password="testing_password1"
        )

        self.test_post = Post.objects.create(
            title="testing title_1",
            content="testing content_1",
            author=self.test_user
        )

        self.test_user2 = get_user_model().objects.create_user(
            username="testing_user_2",
            email="testing2@mail.com",
            password="testing_password2"
        )

        self.test_post2 = Post.objects.create(
            title="testing title_2",
            content="testing content_2",
            author=self.test_user2
        )

    def test_user_posts_list(self):
        resp = self.client.get('/posts/testing_user_1/')
        self.assertContains(resp, 'testing title_1')
        self.assertNotContains(resp, 'testing title_2')
        self.assertContains(resp, 'testing_user_1')
        self.assertNotContains(resp, 'testing_user_2')


class Pagination(TestCase):
    def setUp(self):

        self.test_user = get_user_model().objects.create_user(
            username="testing_user",
            email="testing@mail.com",
            password="testing_password"
        )

        for i in range(10, 0, -1):
            self.test_post = Post.objects.create(
                title="testing title_" + str(i),
                content="testing content_" + str(i),
                author=self.test_user
            )

    def test_pagination_status_code(self):
        resp = self.client.get('/?page=2')
        self.assertEqual(resp.status_code, 200)

    def test_pagination_list(self):
        resp = self.client.get('/?page=2')
        self.assertContains(resp, 'testing title_10')
        self.assertContains(resp, 'testing content_6')
        self.assertNotContains(resp, 'testing title_2')


class Profile(TestCase):
    def setUp(self):
        self.test_user = get_user_model().objects.create_user(
            username="testing_user",
            email="testing@mail.com",
            password="testing_password"
        )

        login = self.client.login(
            username='testing_user',
            password='testing_password'
        )

    def test_profile_status_code(self):
        resp = self.client.get('/profile/')
        self.assertEqual(resp.status_code, 200)

    def test_profile_name_status_code(self):
        resp = self.client.get(reverse('profile'))
        self.assertEqual(resp.status_code, 200)

    def test_profile_change_items(self):
        resp = self.client.post('/profile/', {
            'username': 'updated_user',
            'email': 'updated_mail@mail.com'
        })
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'updated_user')
        self.assertContains(resp, 'updated_mail@mail.com')
        self.assertNotContains(resp, 'testing_user')
        self.assertNotContains(resp, 'testing@mail.com')

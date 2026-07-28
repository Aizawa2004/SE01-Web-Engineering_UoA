from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from blog.models import Post


class RegistrationViewTests(TestCase):
    def test_get_register_page_shows_form_fields(self):
        response = self.client.get(reverse("accounts:register"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'name="username"')
        self.assertContains(response, 'name="password1"')
        self.assertContains(response, 'name="password2"')
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_post_valid_registration_creates_user_and_redirects(self):
        response = self.client.post(
            reverse("accounts:register"),
            data={
                "username": "newuser",
                "password1": "StrongPass123!",
                "password2": "StrongPass123!",
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(get_user_model().objects.filter(username="newuser").exists())

    def test_post_invalid_registration_rerenders_errors(self):
        response = self.client.post(
            reverse("accounts:register"),
            data={
                "username": "",
                "password1": "StrongPass123!",
                "password2": "mismatch",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This field is required.")
        self.assertContains(response, "The two password fields didn’t match.")
        self.assertFalse(get_user_model().objects.exists())


class LoginLogoutViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="alice", password="password123"
        )

    def test_get_login_page_shows_form_fields(self):
        response = self.client.get(reverse("accounts:login"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'name="username"')
        self.assertContains(response, 'name="password"')
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_post_login_redirects_for_valid_credentials(self):
        response = self.client.post(
            reverse("accounts:login"),
            data={"username": "alice", "password": "password123"},
        )

        self.assertEqual(response.status_code, 302)

    def test_logout_requires_post(self):
        response = self.client.get(reverse("accounts:logout"))

        self.assertNotEqual(response.status_code, 200)

    def test_post_logout_logs_user_out(self):
        self.client.login(username="alice", password="password123")
        response = self.client.post(reverse("accounts:logout"))

        self.assertEqual(response.status_code, 302)


class CreatePostAuthGuardTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="alice", password="password123"
        )

    def test_create_requires_login_for_anonymous_user(self):
        response = self.client.get(reverse("post-create"))

        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response["Location"])

    def test_authenticated_user_is_assigned_as_post_author(self):
        self.client.login(username="alice", password="password123")
        response = self.client.post(
            reverse("post-create"),
            data={"title": "Auth title", "body": "Auth body"},
        )

        self.assertEqual(response.status_code, 302)
        post = Post.objects.get(title="Auth title")
        self.assertEqual(post.author, self.user)

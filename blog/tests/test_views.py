from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from blog.models import Post


class PostCreateViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="alice", password="password123"
        )

    def test_get_renders_empty_form(self):
        response = self.client.get(reverse("post-create"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'name="title"')
        self.assertContains(response, 'name="body"')
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_post_valid_data_saves_post_and_redirects(self):
        response = self.client.post(
            reverse("post-create"),
            data={"title": "New title", "body": "New body content"},
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("post-list"), fetch_redirect_response=False)
        self.assertTrue(Post.objects.filter(title="New title").exists())
        self.assertEqual(Post.objects.get(title="New title").content, "New body content")

    def test_post_invalid_data_rerenders_form_errors(self):
        response = self.client.post(
            reverse("post-create"),
            data={"title": "", "body": "New body content"},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'name="title"')
        self.assertContains(response, 'This field is required.')
        self.assertEqual(Post.objects.count(), 0)

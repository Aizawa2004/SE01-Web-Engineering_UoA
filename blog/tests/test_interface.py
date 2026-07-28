from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from blog.models import Post


class InterfaceTemplateTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="alice", password="password123"
        )

    def test_post_create_page_uses_base_layout_structure(self):
        self.client.login(username="alice", password="password123")
        response = self.client.get(reverse("post-create"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'name="viewport" content="width=device-width, initial-scale=1.0"')
        self.assertContains(response, "<header", html=False)
        self.assertContains(response, "<nav", html=False)
        self.assertContains(response, "<main", html=False)
        self.assertContains(response, "<footer", html=False)

    def test_post_list_renders_html_layout_and_post_cards(self):
        Post.objects.create(
            author=self.user,
            title="Alpha Post",
            content="Alpha content",
        )

        response = self.client.get(reverse("post-list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<main", html=False)
        self.assertContains(response, 'class="post-card"')
        self.assertContains(response, "Alpha Post by alice")

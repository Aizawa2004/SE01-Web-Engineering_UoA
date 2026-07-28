from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Post


class BlogViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="alice", password="password123"
        )
        self.other_user = get_user_model().objects.create_user(
            username="bob", password="password123"
        )
        self.first_post = Post.objects.create(
            author=self.user,
            title="Alpha Post",
            content="Alpha content",
        )
        self.second_post = Post.objects.create(
            author=self.other_user,
            title="Beta Post",
            content="Beta content",
        )
        Post.objects.filter(pk=self.second_post.pk).update(
            created_at=timezone.now() - timedelta(days=1)
        )
        self.second_post.refresh_from_db()

    def test_post_list_returns_all_posts(self):
        response = self.client.get(reverse("post-list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Alpha Post by alice")
        self.assertContains(response, "Beta Post by bob")

    def test_post_list_by_author_filters_posts(self):
        response = self.client.get(
            reverse("post-list-by-author", kwargs={"username": "alice"})
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Alpha Post by alice")
        self.assertNotContains(response, "Beta Post by bob")

    def test_post_list_by_date_filters_posts(self):
        response = self.client.get(
            reverse(
                "post-list-by-date",
                kwargs={"date_str": self.first_post.created_at.date().isoformat()},
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Alpha Post by alice")
        self.assertNotContains(response, "Beta Post by bob")

    def test_post_create_dummy_creates_post_and_redirects(self):
        response = self.client.get(reverse("post-create-dummy"))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("post-list"), fetch_redirect_response=False)
        self.assertTrue(Post.objects.filter(title="Dummy Post").exists())

        list_response = self.client.get(reverse("post-list"))
        self.assertContains(list_response, "Dummy Post by dummy")

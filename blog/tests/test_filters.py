from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from blog.models import Post


class PostListFilterTests(TestCase):
    def setUp(self):
        self.alice = get_user_model().objects.create_user(
            username="alice", password="password123"
        )
        self.bob = get_user_model().objects.create_user(
            username="bob", password="password123"
        )

        self.alice_post = Post.objects.create(
            author=self.alice,
            title="Alpha Launch",
            content="Alpha content",
        )
        self.bob_post = Post.objects.create(
            author=self.bob,
            title="Beta Update",
            content="Beta content",
        )
        Post.objects.filter(pk=self.bob_post.pk).update(
            created_at=timezone.now() - timedelta(days=1)
        )
        self.bob_post.refresh_from_db()

    def test_post_list_filters_by_author_query(self):
        response = self.client.get(reverse("post-list"), {"author": "alice"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Alpha Launch")
        self.assertContains(response, '>alice<')
        self.assertNotContains(response, "Beta Update by bob")

    def test_post_list_filters_by_date_query(self):
        response = self.client.get(
            reverse("post-list"), {"date": self.alice_post.created_at.date().isoformat()}
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Alpha Launch")
        self.assertContains(response, '>alice<')
        self.assertNotContains(response, "Beta Update by bob")

    def test_post_list_filters_by_title_search_query(self):
        response = self.client.get(reverse("post-list"), {"q": "alpha"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Alpha Launch")
        self.assertContains(response, '>alice<')
        self.assertNotContains(response, "Beta Update by bob")

    def test_post_list_context_includes_authors(self):
        response = self.client.get(reverse("post-list"))

        self.assertEqual(response.status_code, 200)
        self.assertIn("authors", response.context)
        self.assertCountEqual(
            [author.username for author in response.context["authors"]],
            ["alice", "bob"],
        )

    def test_post_list_renders_filter_ui(self):
        response = self.client.get(reverse("post-list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'href="?author=alice"')
        self.assertContains(response, 'href="?author=bob"')
        self.assertContains(response, 'type="date"')
        self.assertContains(response, 'type="search"')

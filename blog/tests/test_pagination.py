from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from blog.models import Post


class PostListPaginationTests(TestCase):
	def _pagination_context(self, response):
		for context in response.context:
			if isinstance(context, dict) and "page_obj" in context:
				return context
		return response.context[-1]

	def setUp(self):
		self.alice = get_user_model().objects.create_user(
			username="alice", password="password123"
		)
		self.bob = get_user_model().objects.create_user(
			username="bob", password="password123"
		)

		self.posts = []
		for index in range(10):
			post = Post.objects.create(
				author=self.alice if index < 7 else self.bob,
				title=f"{'Alpha' if index < 7 else 'Beta'} Post {index + 1}",
				content=f"Content {index + 1}",
			)
			self.posts.append(post)

		for offset, post in enumerate(reversed(self.posts)):
			Post.objects.filter(pk=post.pk).update(
				created_at=timezone.now() - timedelta(minutes=offset)
			)

	def test_post_list_paginates_posts(self):
		response = self.client.get(reverse("post-list"))
		context = self._pagination_context(response)

		self.assertEqual(response.status_code, 200)
		self.assertTrue(context["is_paginated"])
		self.assertEqual(context["page_obj"].number, 1)
		self.assertEqual(context["page_obj"].paginator.per_page, 5)
		self.assertEqual(len(context["page_obj"].object_list), 5)
		self.assertContains(response, "Page 1 of 2")
		self.assertContains(response, "Next")
		self.assertNotContains(response, "Previous")

	def test_post_list_paginates_second_page(self):
		response = self.client.get(reverse("post-list"), {"page": 2})
		context = self._pagination_context(response)

		self.assertEqual(response.status_code, 200)
		self.assertTrue(context["is_paginated"])
		self.assertEqual(context["page_obj"].number, 2)
		self.assertEqual(len(context["page_obj"].object_list), 5)
		self.assertContains(response, "Page 2 of 2")
		self.assertContains(response, "Previous")
		self.assertNotContains(response, "Next")

	def test_post_list_author_filter_pagination_preserves_query_params(self):
		response = self.client.get(reverse("post-list"), {"author": "alice"})

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "Next")
		self.assertContains(response, "Page 1 of 2")
		self.assertContains(response, "?author=alice&page=2")

	def test_post_list_author_filter_page_two_preserves_query_params(self):
		response = self.client.get(reverse("post-list"), {"author": "alice", "page": 2})

		self.assertEqual(response.status_code, 200)
		self.assertContains(response, "Previous")
		self.assertContains(response, "Page 2 of 2")
		self.assertNotContains(response, "Next")
		self.assertContains(response, "?author=alice&page=1")

	def test_post_list_search_filter_page_two_preserves_query_params(self):
		response = self.client.get(reverse("post-list"), {"q": "Alpha", "page": 2})
		context = self._pagination_context(response)

		self.assertEqual(response.status_code, 200)
		self.assertEqual(context["page_obj"].number, 2)
		self.assertEqual(len(context["page_obj"].object_list), 2)
		self.assertContains(response, "Previous")
		self.assertNotContains(response, "Next")
		self.assertContains(response, "?q=Alpha&page=1")

	def test_post_list_filters_then_paginates(self):
		response = self.client.get(
			reverse("post-list"), {"q": "Alpha", "page": 2}
		)
		context = self._pagination_context(response)

		self.assertEqual(response.status_code, 200)
		self.assertEqual(context["page_obj"].number, 2)
		self.assertEqual(len(context["page_obj"].object_list), 2)
		self.assertTrue(all(post.title.startswith("Alpha") for post in context["page_obj"].object_list))

from django.test import TestCase
from django.contrib.auth import get_user_model

from .models import Post


class PostModelTests(TestCase):
	def test_create_post(self):
		user = get_user_model().objects.create_user(
			username="alice", password="password123"
		)

		post = Post.objects.create(
			author=user,
			title="My first post",
			content="Hello, The Blogs!",
		)

		self.assertEqual(post.author, user)
		self.assertEqual(post.title, "My first post")
		self.assertEqual(post.content, "Hello, The Blogs!")
		self.assertIsNotNone(post.created_at)

	def test_post_str_returns_title(self):
		user = get_user_model().objects.create_user(
			username="bob", password="password123"
		)

		post = Post.objects.create(
			author=user,
			title="Readable admin title",
			content="Body",
		)

		self.assertEqual(str(post), "Readable admin title")

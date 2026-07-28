from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from blog.models import Post


class PostListHtmxTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="alice", password="password123"
        )
        for index in range(6):
            Post.objects.create(
                author=self.user,
                title=f"Alpha Post {index + 1}",
                content=f"Content {index + 1}",
            )

    def test_post_list_regular_request_renders_full_layout(self):
        response = self.client.get(reverse("post-list"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blog/post_list.html")
        self.assertContains(response, '<header class="site-header">', html=False)
        self.assertContains(response, '<footer class="site-footer">', html=False)
        self.assertContains(response, 'id="post-list-container"')

    def test_post_list_htmx_request_renders_partial_only(self):
        response = self.client.get(
            reverse("post-list"),
            HTTP_HX_REQUEST="true",
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blog/partials/post_list_content.html")
        self.assertNotContains(response, '<header class="site-header">', html=False)
        self.assertNotContains(response, '<footer class="site-footer">', html=False)
        self.assertContains(response, 'class="post-grid"')

    def test_post_list_renders_htmx_attributes_for_filters_and_pagination(self):
        response = self.client.get(reverse("post-list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'hx-get="/"')
        self.assertContains(response, 'hx-target="#post-list-container"')
        self.assertContains(response, 'hx-trigger="change from:select, change from:input[type=date], keyup changed delay:500ms from:input[name=\'q\']"')
        self.assertContains(response, 'hx-include="[name=\'q\'], [name=\'author\'], [name=\'date\']"')
        self.assertContains(response, 'hx-push-url="true"')

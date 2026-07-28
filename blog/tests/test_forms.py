from django.test import TestCase

from blog.forms import PostForm


class PostFormTests(TestCase):
    def test_form_valid_with_title_and_body(self):
        form = PostForm(
            data={"title": "Valid title", "body": "A valid body for the post."}
        )

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["title"], "Valid title")
        self.assertEqual(form.cleaned_data["body"], "A valid body for the post.")

    def test_form_invalid_when_title_is_blank(self):
        form = PostForm(data={"title": "", "body": "A valid body for the post."})

        self.assertFalse(form.is_valid())
        self.assertIn("title", form.errors)

    def test_form_invalid_when_title_exceeds_100_chars(self):
        form = PostForm(
            data={"title": "x" * 101, "body": "A valid body for the post."}
        )

        self.assertFalse(form.is_valid())
        self.assertIn("title", form.errors)

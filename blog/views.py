from datetime import datetime

from django.contrib.auth import get_user_model
from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect

from .forms import PostForm
from .models import Post


def _format_posts(posts):
	lines = [f"{post.title} by {post.author.username}" for post in posts]
	return HttpResponse("\n".join(lines) if lines else "No posts yet.")


def post_list(request):
	posts = Post.objects.select_related("author").all()
	return _format_posts(posts)


def post_list_by_author(request, username):
	posts = Post.objects.select_related("author").filter(author__username=username)
	return _format_posts(posts)


def post_list_by_date(request, date_str):
	date = datetime.strptime(date_str, "%Y-%m-%d").date()
	posts = Post.objects.select_related("author").filter(created_at__date=date)
	return _format_posts(posts)


def post_create_dummy(request):
	user_model = get_user_model()
	user, _ = user_model.objects.get_or_create(username="dummy")
	user.set_unusable_password()
	user.save(update_fields=["password"])
	Post.objects.create(
		author=user,
		title="Dummy Post",
		content="This is a dummy post.",
	)
	return redirect("post-list")


def post_create(request):
	if request.method == "POST":
		form = PostForm(request.POST)
		if form.is_valid():
			author = get_user_model().objects.order_by("id").first()
			if author is None:
				author = get_user_model().objects.create_user(
					username="anonymous", password="password123"
				)
			Post.objects.create(
				author=author,
				title=form.cleaned_data["title"],
				content=form.cleaned_data["body"],
			)
			return redirect("post-list")
	else:
		form = PostForm()

	return render(request, "blog/post_create.html", {"form": form})

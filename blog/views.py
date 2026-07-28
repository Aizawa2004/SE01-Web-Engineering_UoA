from datetime import datetime

from django.core.paginator import Paginator
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import PostForm
from .models import Post


POSTS_PER_PAGE = 5


def _build_querystring(request):
	query_params = request.GET.copy()
	query_params.pop("page", None)
	return query_params.urlencode()


def post_list(request):
	posts = Post.objects.select_related("author").order_by("-created_at")
	author_username = request.GET.get("author", "").strip()
	date_str = request.GET.get("date", "").strip()
	search_query = request.GET.get("q", "").strip()

	if author_username:
		posts = posts.filter(author__username=author_username)

	if date_str:
		try:
			selected_date = datetime.strptime(date_str, "%Y-%m-%d").date()
		except ValueError:
			posts = posts.none()
		else:
			posts = posts.filter(created_at__date=selected_date)

	if search_query:
		posts = posts.filter(title__icontains=search_query)

	paginator = Paginator(posts, POSTS_PER_PAGE)
	page_obj = paginator.get_page(request.GET.get("page"))

	authors = (
		get_user_model()
		.objects.filter(post__isnull=False)
		.distinct()
		.order_by("username")
	)
	querystring = _build_querystring(request)
	template_name = "blog/partials/post_list_content.html" if request.htmx else "blog/post_list.html"
	return render(
		request,
		template_name,
		{
			"posts": page_obj.object_list,
			"authors": authors,
			"page_title": "All Posts",
			"selected_author": author_username,
			"selected_date": date_str,
			"search_query": search_query,
			"page_obj": page_obj,
			"paginator": paginator,
			"is_paginated": page_obj.has_other_pages(),
			"querystring": querystring,
		},
	)


def post_list_by_author(request, username):
	posts = Post.objects.select_related("author").filter(author__username=username)
	return render(
		request,
		"blog/post_list.html",
		{"posts": posts, "page_title": f"Posts by {username}"},
	)


def post_list_by_date(request, date_str):
	try:
		date = datetime.strptime(date_str, "%Y-%m-%d").date()
	except ValueError:
		posts = Post.objects.none()
		page_title = f"Posts on {date_str}"
	else:
		posts = Post.objects.select_related("author").filter(created_at__date=date)
		page_title = f"Posts on {date.isoformat()}"

	return render(
		request,
		"blog/post_list.html",
		{"posts": posts, "page_title": page_title},
	)


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


@login_required
def post_create(request):
	if request.method == "POST":
		form = PostForm(request.POST)
		if form.is_valid():
			Post.objects.create(
				author=request.user,
				title=form.cleaned_data["title"],
				content=form.cleaned_data["body"],
			)
			return redirect("post-list")
	else:
		form = PostForm()

	return render(request, "blog/post_create.html", {"form": form})

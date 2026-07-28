from django.urls import path

from . import views

urlpatterns = [
	path("", views.post_list, name="post-list"),
	path("author/<str:username>/", views.post_list_by_author, name="post-list-by-author"),
	path("date/<str:date_str>/", views.post_list_by_date, name="post-list-by-date"),
	path("post/new/", views.post_create_dummy, name="post-create-dummy"),
]
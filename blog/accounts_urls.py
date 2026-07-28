from django.urls import path

from .auth_views import BlogLoginView, logout_view, register

app_name = "accounts"

urlpatterns = [
	path("register/", register, name="register"),
	path("login/", BlogLoginView.as_view(), name="login"),
	path("logout/", logout_view, name="logout"),
]
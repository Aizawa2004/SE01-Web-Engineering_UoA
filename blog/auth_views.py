from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST


class BlogLoginView(LoginView):
	template_name = "accounts/login.html"
	form_class = AuthenticationForm
	redirect_authenticated_user = True

	def get_success_url(self):
		return reverse_lazy("post-list")


def register(request):
	if request.method == "POST":
		form = UserCreationForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			return redirect("post-list")
	else:
		form = UserCreationForm()

	return render(request, "accounts/register.html", {"form": form})


@require_POST
def logout_view(request):
	logout(request)
	return redirect("post-list")
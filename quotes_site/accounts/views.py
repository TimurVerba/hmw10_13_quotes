from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages

from .forms import RegisterForm, LoginForm


class RegisterView(View):
    template_name = 'accounts/register.html'
    form_class = RegisterForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(to="quotes:home")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        return render(request, self.template_name, {"form": self.form_class})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            username = form.cleaned_data["username"]
            messages.success(request, f"Congratulations " + username + "! Your account has been created successfully")
            return redirect(to="quotes:home")
        return render(request, self.template_name, {"form": form})


class LoginView(View):
    template_name = 'accounts/login.html'
    form_class = LoginForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(to="quotes:home")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        return render(request, self.template_name, {"form": self.form_class})

    def post(self, request):
        form = self.form_class(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect(to="quotes:home")
        return render(request, self.template_name, {"form": form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, "Goodbye! Please come back soon!")
        return redirect(to="quotes:home")

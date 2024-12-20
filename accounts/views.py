from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from quiz.services import get_user_quizzes_results


@method_decorator(login_required, name="dispatch")
class Account(View):
    def get(self, request):
        context = {}
        quizzes = get_user_quizzes_results(request.user)
        context["quizzes"] = quizzes
        return render(request, "accounts/account.html", context)


class Login(View):
    def get(self, request):
        context = {}
        form = AuthenticationForm()
        context["form"] = form
        return render(request, "accounts/login.html", context)

    def post(self, request):
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect("home")
        context = {"form": form}
        return render(request, "accounts/login.html", context)


class Logout(View):
    def get(self, request):
        logout(request)
        return redirect("home")


class Registration(View):
    def get(self, request):
        context = {}
        form = UserCreationForm()
        context["form"] = form
        return render(request, "accounts/registration.html", context)

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
        else:
            context = {"form": form}
            return render(request, "accounts/registration.html", context)

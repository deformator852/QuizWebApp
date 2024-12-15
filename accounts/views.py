from django.shortcuts import render
from django.views import View
from django.contrib.auth.forms import AuthenticationForm


class Login(View):
    def get(self, request):
        context = {}
        form = AuthenticationForm()
        context["form"] = form
        return render(request, "accounts/login.html", context)

    def post(self, request):
        pass


class Logout(View):
    def post(self, request):
        pass


class Registration(View):
    def get(self, request):
        return render(request, "accounts/registration.html")

    def post(self, request):
        pass

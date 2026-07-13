from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth import logout
from django.shortcuts import redirect

from .forms import RegisterForm, LoginForm


def home(request):
    return render(request, "home.html")


def register_view(request):

    if request.method == "POST":

        form = RegisterForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")

    else:
        form = RegisterForm()

    return render(
        request,
        "accounts/register.html",
        {
            "form": form
        }
    )


def login_view(request):

    if request.method == "POST":

        form = LoginForm(request, data=request.POST)

        if form.is_valid():

            login(request, form.get_user())

            return redirect("home")

    else:

        form = LoginForm(request)

    return render(
        request,
        "accounts/login.html",
        {
            "form": form
        }
    )

def logout_view(request):
    if request.method == "POST":
        logout(request)

    return redirect("home")
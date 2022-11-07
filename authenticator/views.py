from django.shortcuts import render, redirect
from .forms import NewUserForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from pprint import pprint
# HTTPresponse
from django.http import HttpResponse
# Create your views here.
from django.contrib.auth.forms import AuthenticationForm


def login_request(request):
    """ REDIRECT IF USER ALREADY LOGGED IN """
    if request.user.is_authenticated:
        return redirect("/posts/index")
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("/posts/index")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="authenticator/templates/login.html", context={"login_form": form})


def register_request(request):
    if request.user.is_authenticated:
        return redirect("/posts/index")
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("/posts/:homepage")
        messages.error(
            request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(request=request, template_name="authenticator/templates/register.html", context={"register_form": form})

def logout_request(request):
    if not request.user.is_authenticated:
        return redirect("/posts/index")

    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("/posts/index")
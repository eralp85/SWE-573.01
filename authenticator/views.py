from django.shortcuts import render, redirect
from .forms import NewUserForm, UserEditForm, ProfileEditForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import auth
from django.contrib import messages
from pprint import pprint
from .models import Profile
from django.contrib.auth.decorators import login_required
# HTTPresponse
from django.http import HttpResponse
# Create your views here.
from django.contrib.auth.forms import AuthenticationForm


def login_request(request):
    if request.user.is_authenticated:
        return redirect("/home")
    """ REDIRECT IF USER ALREADY LOGGED IN """
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are logged in as {username}. Welcome!")
                return redirect("/home")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="authenticator/templates/login.html", context={"login_form": form})


def register_request(request):
    if request.user.is_authenticated:
        return redirect("/")
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            # a = Author()
            # a.user_id = user.id
            # a.email = user.email
            # a.first_name = "test"
            # a.last_name = "hehehe"
            # a.save()

            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("/")
        else:
            messages.error(request, form.errors)
        messages.error(
            request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(request=request, template_name="authenticator/templates/register.html",
                  context={"register_form": form})


def logout_request(request):
    # if not request.user.is_authenticated:
    #     return redirect("/")
    #
    # logout(request)
    # messages.info(request, "Logged out successfully!"),
    auth.logout(request)
    return redirect("login")


def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,
                                 data=request.POST)
        profile_form = ProfileEditForm(
                                    instance=request.user.profile,
                                    data=request.POST,
                                    files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'edit.html',
                  {'user_form': user_form,
                   'profile_form': profile_form},)
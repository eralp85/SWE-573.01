from django.shortcuts import render


# Create your views here.

def users__list(request):
    return render(request, 'users_/users__list.html', {})
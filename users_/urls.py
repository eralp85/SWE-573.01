from django.urls import path
from . import views

urlpatterns = [
    path('', views.users__list, name='users__list'),
]
from django.urls import path
from django.conf.urls import include, url
from . import views
from authenticator.views import *
from .views import *

urlpatterns = [

    path('home', views.post_list, name='post_list'),
    path('<int:labels>/', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('post/<int:pk>/remove/', views.post_remove, name='post_remove'),
    path('post/<int:pk>/comment/', views.add_comment_to_post, name='add_comment_to_post'),
    path('post/search/', views.search, name='search'),
    path('myresearch/', views.my_research, name='my_research'),
    path('myaccount/', views.my_account, name='my_account'),
    path('faq/', views.faq, name='faq'),
    path('macro_economy/', views.macro_economy, name='macro_economy'),
    path('equity/', views.equity, name='equity'),
    path('fixed_income/', views.fixed_income, name='fixed_income'),
    path('company_news/', views.company_news, name='company_news'),
    path('post/<int:pk>/share/', views.post_share, name='post_share'),
    path('tag/<slug:tag_slug>/', views.post_list, name='post_list_by_tag'),
    path("logout/", logout_request, name="logout"),
    path("like/<int:pk>", views.like_post, name="like_post"),
    path('users/', views.user_list, name='user_list'),
    path('users/<username>/', views.user_detail, name='user_detail'),
    path('users/follow', views.user_follow, name='user_follow'),
    path('', views.post_list, name='post_list_'),
]

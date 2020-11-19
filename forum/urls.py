from forum.views import login
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('posts/', views.posts, name='posts'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('users/', views.users, name='users'),
    path('all_users/', views.all_users, name='all_users')
]
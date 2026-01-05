from django.contrib import admin
from django.urls import path,include
from .views import *

urlpatterns = [
    path('', login_view, name='login'),
    path('schools/', schools_view, name='schools'),
    path('logout/', logout_view, name='logout'),
    path('users/', users_view, name='users'),
    path('users/add/', add_user, name='add_user'),
    path('users/delete/', delete_user, name='delete_user'),
    path('control_book/',control_book, name='controlB'),
    path('BookIssue/',BookIssiuе, name='BookIssiue'),
    path('control_book/edit/', edit_book, name='edit_book'),
    path('control_book/delete/', delete_book, name='delete_book'),
    path('no-access/', no_access, name='no_access'),
]
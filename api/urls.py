from django.contrib import admin
from django.urls import path
from api import views

urlpatterns = [
    path('user/', views.UserAPI.as_view()),
    path('get-all-users/', views.UserAPI.get_users_all, name='get_users_all'),
	path('get-user/<int:uid>', views.UserAPI.get_user, name='get_user'),
    path('update-users/<int:uid>', views.UserAPI.update_user, name='update_user'),
	path('delete-user/<int:uid>', views.UserAPI.delete_user, name='delete_user'),
	path('delete-all/', views.UserAPI.delete_all, name='delete_all'),
]
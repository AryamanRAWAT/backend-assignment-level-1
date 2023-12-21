from django.contrib import admin
from django.urls import path
from api import views

urlpatterns = [
    path('create-user/', views.post_user, name='post_user'),
    path('get-all-users/', views.get_users_all, name='get_users_all'),
	path('get-user/<int:uid>', views.get_user, name='get_user'),
    path('update-users/<int:uid>', views.update_user, name='update_user'),
	path('delete-user/<int:uid>', views.delete_user, name='delete_user'),
	path('delete-all/', views.delete_all, name='delete_all'),
]
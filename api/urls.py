from django.contrib import admin
from django.urls import path
from api import views

urlpatterns = [
    path('user/', views.UserAPI.as_view()),
	path('user/<int:pk>', views.UserAPI.as_view()),
]
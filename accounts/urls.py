from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import (
    login_page,
    register_page,
)

urlpatterns = [
    path('login/', login_page, name='login'),
    path('register/', register_page, name='register'),
    path('', LogoutView.as_view(), name='logout'),
]

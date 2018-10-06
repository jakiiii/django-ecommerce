from django.conf import settings
from django.urls import path
from django.contrib.auth.views import LogoutView

from .views import (
    login_page,
    register_page,
    guest_register_view,
)

urlpatterns = [
    path('login/', login_page, name='login'),
    path('register/', register_page, name='register'),
    path('register/guest/', guest_register_view, name='guest-register'),
    path('logout/', LogoutView.as_view(), {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),
]

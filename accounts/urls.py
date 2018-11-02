from django.conf import settings
from django.urls import path
from django.contrib.auth.views import LogoutView

from .views import (
    UserLoginView,
    UserRegistrationView,
    guest_register_view,
    AccountsHomeView,
    AccountActivateView
)

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('register/guest/', guest_register_view, name='guest-register'),
    path('', AccountsHomeView.as_view(), name='user-account'),
    path('email/confirmed/<key>/', AccountActivateView.as_view(), name='email-activate'),
    path('logout/', LogoutView.as_view(), {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),
]

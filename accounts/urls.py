from django.conf import settings
from django.urls import path
from django.views.generic import RedirectView
from django.contrib.auth.views import LogoutView

from .views import (
    UserLoginView,
    UserRegistrationView,
    guest_register_view,
    AccountsHomeView,
)

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('register/guest/', guest_register_view, name='guest-register'),
    path('accounts/', RedirectView.as_view(url='/account')),
    path('account/', AccountsHomeView.as_view(), name='user-account'),
    path('logout/', LogoutView.as_view(), {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),
]

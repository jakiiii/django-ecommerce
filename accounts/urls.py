from django.conf import settings
from django.urls import path
from django.contrib.auth.views import LogoutView

from products.views import UserProductHistoryView

from .views import (
    UserLoginView,
    UserRegistrationView,
    GuestRegisterForm,
    AccountsHomeView,
    UserInfoUpdateView,
    AccountActivateView
)

urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('register/guest/', GuestRegisterForm.as_view(), name='guest-register'),
    path('', AccountsHomeView.as_view(), name='user-account'),
    path('email/confirmed/<key>/', AccountActivateView.as_view(), name='email-activate'),
    path('email/resend-activation/', AccountActivateView.as_view(), name='resend-activation'),
    path('update/name/', UserInfoUpdateView.as_view(), name='update-user-name'),
    path('history/product/', UserProductHistoryView.as_view(), name='product-history'),
    path('logout/', LogoutView.as_view(), {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),
]

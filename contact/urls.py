from django.urls import path

from .views import (
    contact_page,
    login_page,
    register_page,
)

urlpatterns = [
    path('', contact_page, name='contact'),
    path('login/', login_page, name='login'),
    path('register', register_page, name='register'),
]

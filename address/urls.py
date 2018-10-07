from django.urls import path
from .views import (
    checkout_address_create_view,
    checkout_address_reuse_view,
)

urlpatterns = [
    path('checkout/address/create/', checkout_address_create_view, name='checkout-address'),
    path('checkout/address/reuse/', checkout_address_reuse_view, name='checkout-reuse')
]

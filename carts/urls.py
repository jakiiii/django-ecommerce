from django.urls import path

from .views import (
    cart_home,
    cart_details_api_view,
    cart_update,
    checkout_home,
    cart_done,
)

urlpatterns = [
    path('', cart_home, name='cart'),
    path('api/cart/', cart_details_api_view, name='api-cart'),
    path('update/', cart_update, name='cart-update'),
    path('checkout/', checkout_home, name='checkout'),
    path('checkout/success/', cart_done, name='success'),
]

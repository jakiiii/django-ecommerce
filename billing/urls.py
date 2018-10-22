from django.urls import path
from billing.views import (
    payment_method_view,
    payment_method_create_view
)


urlpatterns = [
    path('billing/payment-method/', payment_method_view, name="payment-method"),
    path('billing/payment-method/create/', payment_method_create_view, name="payment-method-endpoint")
]

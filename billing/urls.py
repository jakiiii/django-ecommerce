from django.urls import path
from billing.views import payment_method_view


urlpatterns = [
    path('billing/payment-method/', payment_method_view, name="payment-method")
]

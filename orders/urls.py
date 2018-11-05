from django.urls import path

from .views import (
    OrderListView,
    OrderDetailView
)

urlpatterns = [
    path('order/list/', OrderListView.as_view(), name='order_list'),
    path('order/details/<str:order_id>/', OrderDetailView.as_view(), name='order_detail'),
]

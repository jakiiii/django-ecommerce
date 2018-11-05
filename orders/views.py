from django.shortcuts import render, Http404
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from billing.models import BillingProfile
from .models import Order


# Create your views here.
class OrderListView(LoginRequiredMixin, ListView):
    template_name = 'orders/order_list.html'
    model = Order

    def get_queryset(self):
        return Order.objects.by_request(self.request).not_created()


class OrderDetailView(LoginRequiredMixin, DetailView):
    template_name = 'orders/order_details.html'
    model = Order

    def get_object(self, queryset=None):
        qs = Order.objects.by_request(self.request).filter(order_id=self.kwargs.get('order_id'))
        if qs.count() == 1:
            return qs.first()
        return Http404

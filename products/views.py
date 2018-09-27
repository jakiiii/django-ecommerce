from django.shortcuts import render
from django.views.generic import ListView

from .models import Product


# Create your views here.
class ProductListView(ListView):
    template_name = 'products/list.html'
    queryset = Product.objects.all()
    context_object_name = 'product_list'

    def get_context_data(self, *args, **kwargs):
        context = super(ProductListView, self).get_context_data(*args, **kwargs)
        return context


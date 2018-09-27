from django.shortcuts import render, Http404
from django.views.generic import ListView, DetailView

from .models import Product


# Create your views here.
class ProductListView(ListView):
    template_name = 'products/list.html'
    queryset = Product.objects.all()
    context_object_name = 'product_list'

    def get_context_data(self, *args, **kwargs):
        context = super(ProductListView, self).get_context_data(*args, **kwargs)
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ProductDetailView, self).get_context_data(*args, **kwargs)
        # context['title'] = '{}'.format(self.get_object().title)
        context['title'] = 'Product Details'
        return context

    # def get_object(self, *args, **kwargs):
    #     pk = self.kwargs.get('pk')
    #     instance = Product.objects.get_by_id(pk)
    #     if instance is None:
    #         raise Http404("Page not found")
    #     return instance


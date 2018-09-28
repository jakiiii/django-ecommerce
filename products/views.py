from django.shortcuts import render, Http404
from django.views.generic import ListView, DetailView

# from analytics.mixins import ObjectViewedMixin

from .models import Product


# Create your views here.
class ProductListFeaturedView(ListView):
    template_name = 'products/list.html'

    def get_queryset(self, *args, **kwargs):
        return Product.objects.all().featured()


class ProductDetailFeaturedView(DetailView):
    queryset = Product.objects.all().featured()
    template_name = 'products/product-detail-featured.html'

    # def get_queryset(self, *args, **kwargs):
    #     return Product.objects.featured()

    def get_context_data(self, *args, **kwargs):
        context = super(ProductDetailFeaturedView, self).get_context_data(*args, **kwargs)
        context['title'] = '{}'.format(self.get_object().title)
        return context


class ProductListView(ListView):
    model = Product
    template_name = 'products/list.html'
    context_object_name = 'product_list'

    def get_context_data(self, *args, **kwargs):
        context = super(ProductListView, self).get_context_data(*args, **kwargs)
        return context


class ProductDetailView(DetailView):
    template_name = 'products/product_detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ProductDetailView, self).get_context_data(*args, **kwargs)
        context['title'] = '{}'.format(self.get_object().title)
        return context

    def get_object(self, *args, **kwargs):
        pk = self.kwargs.get('pk')
        instance = Product.objects.get_by_id(pk)
        if instance is None:
            raise Http404("Page not found")
        return instance


class ProductDetailSlugView(DetailView):
    queryset = Product.objects.all()
    template_name = 'products/product_detail.html'

    def get_context_data(self, *args, **kwargs):
        context = super(ProductDetailSlugView, self).get_context_data(*args, **kwargs)
        context['title'] = '{}'.format(self.get_object().title)
        return context

from django.shortcuts import render

from .models import Cart


# Create your views here.
def cart_home(request):
    cart_obj = Cart.objects.new_cart_or_get(request)
    template_name = 'carts/cart_home.html'
    context = {}
    return render(request, template_name, context)

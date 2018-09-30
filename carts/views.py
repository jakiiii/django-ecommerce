from django.shortcuts import render

from .models import Cart


# Create your views here.
def cart_home(request):
    cart_obj, new_obj = Cart.objects.new_cart_or_get(request)
    products = cart_obj.products.all()
    total = 0
    for x in products:
        total += x.price
    cart_obj.total = total
    cart_obj.save()
    template_name = 'carts/cart_home.html'
    context = {}
    return render(request, template_name, context)

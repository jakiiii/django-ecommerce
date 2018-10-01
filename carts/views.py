from django.shortcuts import render, redirect

from .models import Cart
from products.models import Product
from orders.models import Order


# Create your views here.
def cart_home(request):
    cart_obj, new_obj = Cart.objects.new_cart_or_get(request)
    template_name = 'carts/cart_home.html'
    context = {
        "cart": cart_obj
    }
    return render(request, template_name, context)


def cart_update(request):
    product_id = request.POST.get('product')
    if product_id is not None:
        try:
            product_obj = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            print('product is gone!? May be technical bug! We will fixed sooner.')
            return redirect('cart')
        cart_obj, new_obj = Cart.objects.new_cart_or_get(request)
        if product_obj in cart_obj.products.all():
            cart_obj.products.remove(product_obj)
            request.session['cart_items'] = cart_obj.products.count()
        else:
            cart_obj.products.add(product_obj)
            request.session['cart_items'] = cart_obj.products.count()
    # return redirect(product_obj.get_absolute_url())
    return redirect('cart')


def checkout_home(request):
    cart_obj, cart_created = Cart.objects.new_cart_or_get(request)
    order_obj = None
    if cart_created or cart_obj.products.count() == 0:
        return redirect('cart')
    else:
        order_obj, order_new_obj = Order.objects.get_or_create(cart=cart_obj)
    template_name = 'carts/checkout.html'
    context = {
        'object': order_obj
    }
    return render(request, template_name, context)

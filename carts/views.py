from django.shortcuts import render, redirect

from .models import Cart
from products.models import Product


# Create your views here.
def cart_home(request):
    cart_obj, new_obj = Cart.objects.new_cart_or_get(request)
    # products = cart_obj.products.all()
    # total = 0
    # for x in products:
    #     total += x.price
    # cart_obj.total = total
    # cart_obj.save()
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


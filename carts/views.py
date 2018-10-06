from django.shortcuts import render, redirect

from .models import Cart
from accounts.models import GuestEmail
from products.models import Product
from orders.models import Order
from billing.models import BillingProfile

from accounts.forms import LoginForm, GuestForm


# Create your views here.
def cart_home(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
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
        cart_obj, new_obj = Cart.objects.new_or_get(request)
        if product_obj in cart_obj.products.all():
            cart_obj.products.remove(product_obj)
            request.session['cart_items'] = cart_obj.products.count()
        else:
            cart_obj.products.add(product_obj)
            request.session['cart_items'] = cart_obj.products.count()
    # return redirect(product_obj.get_absolute_url())
    return redirect('cart')


def checkout_home(request):
    template_name = 'carts/checkout.html'
    cart_obj, cart_created = Cart.objects.new_or_get(request)
    order_obj = None
    if cart_created or cart_obj.products.count() == 0:
        return redirect('cart')
    user = request.user

    billing_profile = None
    login_form = LoginForm()
    guest_form = GuestForm()
    guest_email_id = request.session.get('guest_email_id')
    if user.is_authenticated:
        billing_profile, billing_profile_created = BillingProfile.objects.get_or_create(user=user, email=user.email)
    elif guest_email_id is not None:
        guest_email_obj = GuestEmail.objects.get(id=guest_email_id)
        billing_profile, billing_guest_profile_created = \
            BillingProfile.objects.get_or_create(email=guest_email_obj.email)
    else:
        print('error check out home in login or guest email!')

    # Lot more completed this order
    if billing_profile is not None:
        order_qs = Order.objects.filter(billing_profile=billing_profile, cart=cart_obj, active=True)
        if order_qs.count() == 1:
            order_obj = order_qs.first()
        else:
            order_obj = Order.objects.create(billing_profile=billing_profile, cart=cart_obj)

    context = {
        'object': order_obj,
        "billing_profile": billing_profile,
        "login_form": login_form,
        "guest_form": guest_form
    }
    return render(request, template_name, context)

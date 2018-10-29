from django.conf import settings
from django.shortcuts import render, redirect
from django.http import JsonResponse

from .models import Cart
from accounts.models import GuestEmail
from products.models import Product
from orders.models import Order
from billing.models import BillingProfile
from address.models import Address

from accounts.forms import UserLoginForm, GuestForm
from address.forms import AddressForm

STRIPE_SECRET_KEY = getattr(settings, "STRIPE_SECRET_KEY", "sk_test_75kkoW8Uu4p38LCZGzyKZ0bB")
STRIPE_PUB_KEY = getattr(settings, "STRIPE_PUB_KEY", "pk_test_PzZbTHlXOfKISCnJOn0edmlI")


# Create your views here.
def cart_details_api_view(request):
    cart_obj, new_obj = Cart.objects.new_or_get(request)
    products = [{
        "id": x.id,
        "url": x.get_absolute_url(),
        "name": x.title,
        "price": x.price} for x in cart_obj.products.all()]

    cart_data = {
        "products": products,
        "subtotal": cart_obj.subtotal,
        "total": cart_obj.total
    }
    return JsonResponse(cart_data)


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
            added = False
            request.session['cart_items'] = cart_obj.products.count()
        else:
            cart_obj.products.add(product_obj)
            added = True
            request.session['cart_items'] = cart_obj.products.count()
    # return redirect(product_obj.get_absolute_url())

        if request.is_ajax():  # Asynchronous Javascript And XML / JSON
            print("ajax request")
            json_data = {
                "added": added,
                "removed": not added,
                "cartItemCount": cart_obj.products.count()
            }
            return JsonResponse(json_data, status=200)
    return redirect('cart')


def checkout_home(request):
    template_name = 'carts/checkout.html'
    cart_obj, cart_created = Cart.objects.new_or_get(request)
    order_obj = None
    if cart_created or cart_obj.products.count() == 0:
        return redirect('cart')

    login_form = UserLoginForm()
    guest_form = GuestForm()
    address_form = AddressForm()
    billing_address_id = request.session.get("billing_address_id", None)
    shipping_address_id = request.session.get("shipping_address_id", None)

    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
    address_qs = None
    has_card = False
    if billing_profile is not None:
        if request.user.is_authenticated:
            address_qs = Address.objects.filter(billing_profile=billing_profile)
        order_obj, order_obj_created = Order.objects.new_or_get(billing_profile, cart_obj)
        if shipping_address_id:
            order_obj.shipping_address = Address.objects.get(id=shipping_address_id)
            del request.session["shipping_address_id"]
        if billing_address_id:
            order_obj.billing_address = Address.objects.get(id=billing_address_id)
            del request.session["billing_address_id"]
        if shipping_address_id or billing_address_id:
            order_obj.save()
        has_card = billing_profile.has_card

    if request.method == "POST":
        "check order is done or not?"
        is_prepared = order_obj.check_done()
        if is_prepared:
            billing_profile.charge(order_obj)
            order_obj.mark_paid()
            request.session["cart_items"] = 0
            del request.session['cart_id']
            if not billing_profile.user:
                '''
                code
                '''
                billing_profile.set_cards_inactive()
            return redirect('success')
        else:
            return redirect('checkout')

    context = {
        'object': order_obj,
        "billing_profile": billing_profile,
        "login_form": login_form,
        "guest_form": guest_form,
        "address_form": address_form,
        "address_qs": address_qs,
        "has_card": has_card,
        "publish_key": STRIPE_PUB_KEY,
    }
    return render(request, template_name, context)


def cart_done(request):
    template_name = 'carts/checkout-done.html'
    context = {}
    return render(request, template_name, context)

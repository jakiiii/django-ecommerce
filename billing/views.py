import stripe
from django.conf import settings
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url
from django.http import JsonResponse, HttpResponse

from .models import BillingProfile, Card

STRIPE_SECRET_KEY = getattr(settings, "STRIPE_SECRET_KEY", "sk_test_75kkoW8Uu4p38LCZGzyKZ0bB")
STRIPE_PUB_KEY = getattr(settings, "STRIPE_PUB_KEY", "pk_test_PzZbTHlXOfKISCnJOn0edmlI")
stripe.api_key = STRIPE_SECRET_KEY


# Create your views here.
def payment_method_view(request):
    template_name = "billing/payment-method.html"

    # if request.user.is_authenticated():
    #     billing_profile = request.user.billingprofile
    #     my_customer_id = billing_profile.customer_id
    billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
    if not billing_profile:
        return redirect('/')

    next_url = None
    next_ = request.GET.get('next')
    if is_safe_url(next_, request.get_host()):
        next_url = next_

    context = {
        "publish_key": STRIPE_PUB_KEY,
        "next_url": next_url
    }
    return render(request, template_name, context)


def payment_method_create_view(request):
    template_name = "billing/payment-method.html"
    context = {
        "publish_key": STRIPE_PUB_KEY
    }
    if request.method == "POST" and request.is_ajax():
        billing_profile, billing_profile_created = BillingProfile.objects.new_or_get(request)
        if not billing_profile:
            return HttpResponse({"message": "Can not find this user!"}, status=401)

        token = request.POST.get("token")
        if token is not None:
            new_card_obj = Card.objects.add_new(billing_profile, token)
        return JsonResponse({"message": "Thank you! Your card is added."})
    return HttpResponse("error", status=401)

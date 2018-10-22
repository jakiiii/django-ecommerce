import stripe
from django.shortcuts import render
from django.utils.http import is_safe_url
from django.http import JsonResponse, HttpResponse

STRIPE_PUB_KEY = "pk_test_PzZbTHlXOfKISCnJOn0edmlI"
stripe.api_key = "sk_test_75kkoW8Uu4p38LCZGzyKZ0bB"


# Create your views here.
def payment_method_view(request):
    template_name = "billing/payment-method.html"

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
        return JsonResponse({"message": "Thank you! Your card is added."})
    return HttpResponse("error", status=401)

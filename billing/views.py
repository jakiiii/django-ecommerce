import stripe
from django.shortcuts import render

STRIPE_PUB_KEY = "pk_test_PzZbTHlXOfKISCnJOn0edmlI"
stripe.api_key = "sk_test_75kkoW8Uu4p38LCZGzyKZ0bB"


# Create your views here.
def payment_method_view(request):
    template_name = "billing/payment-method.html"
    context = {
        "publish_key": STRIPE_PUB_KEY
    }
    if request.method == "POST":
        print(request.method)
    return render(request, template_name, context)

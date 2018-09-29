from django.shortcuts import render


# Create your views here.
def cart_home(request):
    template_name = 'carts/cart_home.html'
    context = {}
    return render(request, template_name, context)

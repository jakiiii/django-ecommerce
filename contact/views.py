from django.shortcuts import render
from django.http import JsonResponse, HttpResponse

from .forms import ContactForm


# Create your views here.
def contact_page(request):
    contact_form = ContactForm(request.POST or None)
    template_name = 'contact/contact.html'
    context = {
        "form": contact_form
    }
    if contact_form.is_valid():
        if request.is_ajax():
            return JsonResponse({"message": "Thank you for your submission."})

    if contact_form.errors:
        errors = contact_form.errors.as_json()
        if request.is_ajax():
            return HttpResponse(errors, status=400, content_type='application/json')

    return render(request, template_name, context)

from django.shortcuts import render

from .forms import ContactForm


# Create your views here.
def contact_page(request):
    contact_form = ContactForm(request.POST or None)
    template_name = 'contact/contact.html'
    context = {
        "form": contact_form
    }
    if contact_form.is_valid():
        print(contact_form.cleaned_data)
    return render(request, template_name, context)

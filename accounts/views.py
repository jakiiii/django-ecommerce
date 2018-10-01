from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.messages.views import messages

from .forms import LoginForm, RegisterForm

User = get_user_model()


# Create your views here.
def login_page(request):
    form = LoginForm(request.POST or None)
    template_name = 'auth/login.html'
    context = {
        "form": form
    }
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('login')
        else:
            print("ERROR")
    return render(request, template_name, context)


def register_page(request):
    form = RegisterForm(request.POST or None)
    template_name = 'auth/register.html'
    context = {
        "form": form
    }
    if form.is_valid():
        print(form.cleaned_data)
        username = form.cleaned_data.get("username")
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        new_user = User.objects.create_user(username, email, password)
        print(new_user)
        messages.success(request, "Your are registered!")
        return redirect('login')
    return render(request, template_name, context)

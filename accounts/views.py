from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, get_user_model
from django.utils.http import is_safe_url
from django.views.generic import FormView, CreateView
from django.contrib.messages.views import messages, SuccessMessageMixin


from .forms import UserLoginForm, UserRegistrationForm, GuestForm
from .models import GuestEmail
from .signals import user_logged_in

User = get_user_model()


# Create your views here.
class UserLoginView(FormView):
    form_class = UserLoginForm
    success_url = '/'
    template_name = 'accounts/login.html'

    def form_valid(self, form):
        next_ = self.request.GET.get('next')
        next_post = self.request.POST.get('next')
        redirect_path = next_ or next_post or None
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        user = authenticate(self.request, email=email, password=password)

        if user is not None:
            login(self.request, user)
            user_logged_in.send(user.__class__, instance=user, request=self.request)
            # user_logged_in.send(user.__class__, instance=user, request=self.request)
            try:
                del self.request.session['guest_email_id']
            except:
                pass
            if is_safe_url(redirect_path, self.request.get_host()):
                return redirect(redirect_path)
        else:
            messages.error(self.request, 'Username or Password is not valid!')
            return redirect('login')
        return super(UserLoginView, self).form_valid(form)


class UserRegistrationView(SuccessMessageMixin, CreateView):
    form_class = UserRegistrationForm
    template_name = 'accounts/register.html'
    success_message = 'Registration successful.'
    success_url = '/login/'


# def login_page(request):
#     form = UserLoginForm(request.POST or None)
#     template_name = 'accounts/login.html'
#     context = {
#         "form": form
#     }
#     next_ = request.GET.get('next')
#     next_post = request.POST.get('next')
#     redirect_path = next_ or next_post or None
#     if form.is_valid():
#         username = form.cleaned_data.get("username")
#         password = form.cleaned_data.get("password")
#         user = authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             try:
#                 del request.session['guest_email_id']
#             except:
#                 pass
#             if is_safe_url(redirect_path, request.get_host()):
#                 return redirect(redirect_path)
#             else:
#                 return redirect('login')
#         else:
#             print("ERROR")
#     return render(request, template_name, context)


# def register_page(request):
#     form = UserRegistrationForm(request.POST or None)
#     template_name = 'accounts/register.html'
#     context = {
#         "form": form
#     }
#     if form.is_valid():
#         print(form.cleaned_data)
#         username = form.cleaned_data.get("username")
#         email = form.cleaned_data.get("email")
#         password = form.cleaned_data.get("password")
#         new_user = User.objects.create_user(username, email, password)
#         print(new_user)
#         messages.success(request, "Your are registered!")
#         return redirect('login')
#     return render(request, template_name, context)


def guest_register_view(request):
    form = GuestForm(request.POST or None)
    template_name = 'accounts/login.html'
    context = {
        "form": form
    }

    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post or None

    if form.is_valid():
        email = form.cleaned_data.get("email")
        new_guest_email = GuestEmail.objects.create(email=email)
        request.session['guest_email_id'] = new_guest_email.id
        if is_safe_url(redirect_path, request.get_host()):
            return redirect(redirect_path)
        else:
            return redirect('register')
    return redirect('register')

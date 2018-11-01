from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.http import is_safe_url
from django.views.generic import FormView, CreateView, DetailView, View
from django.contrib.messages.views import messages, SuccessMessageMixin


from .forms import UserLoginForm, UserRegistrationForm, GuestForm
from .models import GuestEmail, EmailActivation
from .signals import user_logged_in

User = get_user_model()


# Create your views here.
class AccountsHomeView(LoginRequiredMixin, DetailView):
    template_name = 'accounts/home.html'
    login_url = '/account/login/'
    redirect_field_name = 'next'

    def get_object(self, queryset=None):
        return self.request.user


class AccountActivateView(View):
    def get(self, request, *args, **kwargs):
        context = {

        }
        return render(request, 'registration/activation_error.html', context)

    def post(self, request, *args, **kwargs):
        pass


class UserLoginView(FormView):
    form_class = UserLoginForm
    template_name = 'accounts/login.html'
    success_url = '/account/'
    default_next = '/'

    def form_valid(self, form):
        next_ = self.request.GET.get('next')
        next_post = self.request.POST.get('next')
        redirect_path = next_ or next_post or None
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        user = authenticate(self.request, email=email, password=password)

        if user is not None:
            if not user.is_active:
                messages.error(self.request, 'User is Inactive! Please check your email and activation confirm.')
                return super(UserLoginView, self).form_invalid(form)
            login(self.request, user)
            user_logged_in.send(user.__class__, instance=user, request=self.request)
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
    success_url = '/account/login/'


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

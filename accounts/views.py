from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.http import is_safe_url
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.views.generic import FormView, CreateView, DetailView, UpdateView, View
from django.views.generic.edit import FormMixin
from django.contrib.messages.views import messages, SuccessMessageMixin


from .forms import UserLoginForm, UserNameChangeForm, UserRegistrationForm, ReactivateEmailForm, GuestForm
from .models import GuestEmail, EmailActivation
from ecommerce.mixins import NextUrlMixin, RequestFormAttachMixin

User = get_user_model()


# Create your views here.
class AccountsHomeView(LoginRequiredMixin, DetailView):
    template_name = 'accounts/home.html'
    login_url = '/account/login/'
    redirect_field_name = 'next'

    def get_object(self, queryset=None):
        return self.request.user


class AccountActivateView(FormMixin, View):
    success_url = '/account/login/'
    form_class = ReactivateEmailForm
    key = None

    def get(self, request, key=None, *args, **kwargs):
        if key is not None:
            qs = EmailActivation.objects.filter(key__iexact=key)
            confirm_qs = qs.conformable()
            if confirm_qs.count() == 1:
                obj = confirm_qs.first()
                obj.activate()
                messages.success(self.request, "Your email has been confirmed. You can login now.")
                return redirect('login')
            else:
                activated_qs = qs.filter(key__iexact=key, activated=True)
                if activated_qs.exists():
                    reset_link = reverse('password_reset')
                    msg = """Your email has already confirmed!
                    Did you mean <a href="{link}">reset your password</a>?
                    """.format(link=reset_link)
                    messages.info(self.request, mark_safe(msg))
                    return redirect('login')
        context = {
            'form': self.get_form(),
            'key': self.key
        }
        return render(self.request, 'registration/activation_error.html', context)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        msg = "Your account activation link sent. Please check your email."
        messages.success(self.request, msg)
        email = form.cleaned_data.get("email")
        obj = EmailActivation.objects.email_exists(email).first()
        user = obj.user
        new_activation = EmailActivation.objects.create(user=user, email=email)
        new_activation.send_activation()
        return super(AccountActivateView, self).form_valid(form)

    def form_invalid(self, form):
        context = {
            "form": form,
            "key": self.key
        }
        return render(self.request, 'registration/activation_error.html', context)


class UserLoginView(NextUrlMixin, RequestFormAttachMixin, FormView):
    form_class = UserLoginForm
    template_name = 'accounts/login.html'
    success_url = '/account/'
    default_next = '/account/'

    def form_valid(self, form):
        next_path = self.get_next_url()
        return redirect(next_path)


class UserInfoUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'accounts/update_user_info.html'
    form_class = UserNameChangeForm

    def get_object(self):
        return self.request.user

    def get_context_data(self, *args, **kwargs):
        context = super(UserInfoUpdateView, self).get_context_data(*args, **kwargs)
        context['title'] = 'Update Profile Information'
        return context

    def get_success_url(self):
        return reverse('user-account')


class UserRegistrationView(SuccessMessageMixin, CreateView):
    form_class = UserRegistrationForm
    template_name = 'accounts/register.html'
    success_message = 'Registration successful. We send activation instruction on your email.'
    success_url = '/account/login/'


class GuestRegisterForm(NextUrlMixin, RequestFormAttachMixin, CreateView):
    form_class = GuestForm
    default_next = '/register/'

    def get_success_url(self):
        return self.get_next_url()

    def form_invalid(self, form):
        return redirect(self.default_next)

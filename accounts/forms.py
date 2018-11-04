from django import forms
from django.urls import reverse
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.messages.views import messages
from django.utils.safestring import mark_safe

from .models import EmailActivation
from .signals import user_logged_in

User = get_user_model()


# Create your form here.
class UserAdminCreationForm(forms.ModelForm):
    password1 = forms.CharField(max_length=32, label='password', widget=forms.PasswordInput)
    password2 = forms.CharField(max_length=32, label='Password Confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email'
        )

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Password have to match")
        return password2

    def save(self, commit=True):
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email',
            'password',
            'is_active',
            'admin'
        )

    def clean_password(self):
        return self.initial["password"]


class UserLoginForm(forms.Form):
    email = forms.EmailField(max_length=32)
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super(UserLoginForm, self).__init__(*args, **kwargs)

    def clean(self):
        # request = self.request
        data = self.cleaned_data
        email = data.get('email')
        password = data.get('password')
        qs = User.objects.filter(email=email)
        if qs.exists():
            # user email is registered, check email is active or email activation
            not_active = qs.filter(is_active=False)
            if not_active.exists():
                # check email activation
                confirm_email = EmailActivation.objects.filter(email=email)
                is_conformable = confirm_email.conformable().exists()
                if is_conformable:
                    msg = messages.info(self.request, "Please check your email and confirm activation.")
                    raise forms.ValidationError(msg)
                email_confirm_exists = EmailActivation.objects.email_exists(email).exists()
                if email_confirm_exists:
                    msg = messages.info(self.request, "Please resend your conformation email.")
                    raise forms.ValidationError(msg)
                if not is_conformable and not email_confirm_exists:
                    msg = messages.error(self.request, "This user is not active!")
                    raise forms.ValidationError(msg)

        user = authenticate(self.request, email=email, password=password)
        if user is None:
            msg = messages.error(self.request, "Invalid credentials.")
            raise forms.ValidationError(msg)
        login(self.request, user)
        self.user = user
        user_logged_in.send(user.__class__, instance=user, request=self.request)
        try:
            del self.request.session['guest_email_id']
        except:
            pass
        return data

    # def form_valid(self, form):
    #     next_ = self.request.GET.get('next')
    #     next_post = self.request.POST.get('next')
    #     redirect_path = next_ or next_post or None
    #     email = form.cleaned_data.get('email')
    #     password = form.cleaned_data.get('password')
    #     user = authenticate(self.request, email=email, password=password)
    #
    #     if user is not None:
    #         if not user.is_active:
    #             messages.error(self.request, 'User is Inactive! Please check your email and activation confirm.')
    #             return super(UserLoginView, self).form_invalid(form)
    #         login(self.request, user)
    #         user_logged_in.send(user.__class__, instance=user, request=self.request)
    #         try:
    #             del self.request.session['guest_email_id']
    #         except:
    #             pass
    #         if is_safe_url(redirect_path, self.request.get_host()):
    #             return redirect(redirect_path)
    #     else:
    #         messages.error(self.request, 'Username or Password is not valid!')
    #         return redirect('login')
    #     return super(UserLoginView, self).form_valid(form)


class UserRegistrationForm(forms.ModelForm):
    password1 = forms.CharField(max_length=32, label='password', widget=forms.PasswordInput)
    password2 = forms.CharField(max_length=32, label='Password Confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'email'
        )

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Password Don't match!")
        return password2

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.is_active = False  # Send confirmation email via signals
        # obj = EmailActivation.objects.create(user=user)
        # obj.send_activation()
        if commit:
            user.save()
        return user


class ReactivateEmailForm(forms.Form):
    email = forms.EmailField(max_length=32)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = EmailActivation.objects.email_exists(email)
        if not qs.exists():
            register_link = reverse('register')
            msg = """This email does not exists or your account is suspend!. 
            Would you like to <a href={link}>register</a>?""".format(link=register_link)
            raise forms.ValidationError(mark_safe(msg))
        return email


class GuestForm(forms.Form):
    email = forms.EmailField(max_length=32, label="Email", widget=forms.EmailInput(attrs={"class": "form-control"}))

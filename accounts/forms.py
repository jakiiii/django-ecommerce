from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.urls import reverse
from django.utils.safestring import mark_safe

User = get_user_model()

from .models import EmailActivation


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

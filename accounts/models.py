from django.db import models
from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager
)

from django.core.mail import send_mail
from django.template.loader import get_template

from ecommerce.utils import random_string_generator, unique_key_generator


# Create your manager here.
class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None, is_active=True,
                    is_staff=False, is_admin=False):
        if not first_name:
            raise ValueError("Please, type your first name.")
        if not last_name:
            raise ValueError("Please type your last name.")
        if not email:
            raise ValueError('User have to an email address!')
        if not password:
            raise ValueError('User must have a password!')
        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name
        )
        user.set_password(password)
        user.is_active = is_active
        user.staff = is_staff
        user.admin = is_admin
        user.save(using=self._db)
        return user

    def create_staff(self, email, first_name, last_name, password=None):
        user = self.create_user(
            email,
            first_name,
            last_name,
            password=password,
            is_staff=True
        )
        return user

    def create_superuser(self, email, first_name, last_name, password=None):
        user = self.create_user(
            email,
            first_name,
            last_name,
            password=password,
            is_staff=True,
            is_admin=True
        )
        return user


# Create your models here.
class User(AbstractBaseUser):
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)
    email = models.EmailField(max_length=32, unique=True, verbose_name='Email')
    is_active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    objects = UserManager()

    def __str__(self):
        return self.email

    def get_first_name(self):
        return self.first_name

    def get_last_name(self):
        return self.last_name

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    # @property
    # def is_active(self):
    #     return self.active


class EmailActivation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=120)
    key = models.CharField(max_length=120, null=True, blank=True)
    activated = models.BooleanField(default=False)
    forced_expired = models.BooleanField(default=False)
    expired = models.IntegerField(default=7)
    timestamp = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email

    def regenerate(self):
        self.key = None
        self.save()
        if self.key is not None:
            return True
        return False

    def send_activation(self):
        if not self.activated and not self.forced_expired:
            if self.key:
                base_url = getattr(settings, 'BASE_URL')
                key_path = self.key
                path = "{base}{path}".format(base=base_url, path=key_path)
                context = {
                    "path": path,
                    "email": self.email
                }
                txt_ = get_template("registration/emails/verify.txt").render(context)
                html_ = get_template("registration/emails/verify.html").render(context)
                subject = '1-Click Email Activation.'
                from_email = settings.DEFAULT_FROM_EMAIL
                recipient_list = [self.email]
                sent_mail = send_mail(
                    subject,
                    txt_,
                    from_email,
                    recipient_list,
                    html_message=html_,
                    fail_silently=False,
                )
                return sent_mail
        return False


def pre_save_email_activation(sender, instance, *args, **kwargs):
    if not instance.activated and not instance.forced_expired:
        if not instance.key:
            instance.key = unique_key_generator(instance)


class GuestEmail(models.Model):
    email = models.EmailField(max_length=32)
    active = models.BooleanField(default=True)
    update = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

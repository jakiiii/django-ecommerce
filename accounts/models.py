from datetime import timedelta
from django.db import models
from django.conf import settings
from django.db.models.signals import pre_save, post_save
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager
)

from django.core.mail import send_mail
from django.template.loader import get_template
from django.utils import timezone

from ecommerce.utils import random_string_generator, unique_key_generator

DEFAULT_ACTIVATION_DAYS = getattr(settings, 'DEFAULT_ACTIVATION_DAYS', 3)


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


class EmailActivationQuerySet(models.query.QuerySet):
    def conformable(self):
        now = timezone.now()
        start_range = now - timedelta(days=DEFAULT_ACTIVATION_DAYS)
        end_range = now
        return self.filter(
            activated=False,
            forced_expired=False
        ).filter(
            timestamp__gt=start_range,
            timestamp__lte=end_range
        )


class EmailActivationManager(models.Manager):
    def get_queryset(self):
        return EmailActivationQuerySet(self.model, using=self._db)

    def conformable(self):
        return self.get_queryset().conformable()


class EmailActivation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=120)
    key = models.CharField(max_length=120, null=True, blank=True)
    activated = models.BooleanField(default=False)
    forced_expired = models.BooleanField(default=False)
    expired = models.IntegerField(default=3)
    timestamp = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    objects = EmailActivationManager()

    def __str__(self):
        return self.email

    def can_activate(self):
        qs = EmailActivation.objects.filter(pk=self.pk).conformable()
        if qs.exists():
            return True
        return False

    def regenerate(self):
        self.key = None
        self.save()
        if self.key is not None:
            return True
        return False

    def activate(self):
        if self.can_activate():
            # pre activation user signals
            user = self.user
            user.is_active = True
            user.save()
            # post activation signals for user
            self.activated = True
            self.save()
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


pre_save.connect(pre_save_email_activation, sender=EmailActivation)


def post_save_user_created_receiver(sender, instance, created, *args, **kwargs):
    if created:
        obj = EmailActivation.objects.create(user=instance, email=instance.email)
        obj.send_activation()


post_save.connect(post_save_user_created_receiver, sender=User)


class GuestEmail(models.Model):
    email = models.EmailField(max_length=32)
    active = models.BooleanField(default=True)
    update = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

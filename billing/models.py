import stripe
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save, pre_save

from accounts.models import GuestEmail

User = settings.AUTH_USER_MODEL

stripe.api_key = "sk_test_75kkoW8Uu4p38LCZGzyKZ0bB"


# Create your manager here.
class BillingProfileManager(models.Manager):
    def new_or_get(self, request):
        guest_email_id = request.session.get('guest_email_id')
        created = False
        obj = None
        if request.user.is_authenticated:
            'login in user checkout; remember payment staff.'
            obj, created = self.model.objects.get_or_create(user=request.user, email=request.user.email)
        elif guest_email_id is not None:
            'guest user checkout; auto reload payment staff.'
            guest_email_obj = GuestEmail.objects.get(id=guest_email_id)
            obj, created = self.model.objects.get_or_create(email=guest_email_obj.email)
        else:
            print('error check out home in login or guest email!')
        return obj, created


# Create your models here.
class BillingProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    email = models.EmailField(max_length=32)
    active = models.BooleanField(default=True)
    update = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    customer_id = models.CharField(max_length=120, null=True, blank=True)

    objects = BillingProfileManager()

    def __str__(self):
        return self.email


def billing_profile_created_receiver(sender, instance, *args, **kwargs):
    print("ACTUAL API REQUEST send to strip / braintree")
    if not instance.customer_id and instance.email:
        customer = stripe.Customer.create(
            email=instance.email
        )
        print(customer)
        instance.customer_id = customer.id


pre_save.connect(billing_profile_created_receiver, sender=BillingProfile)


def user_created_receiver(sender, instance, created, *args, **kwargs):
    if created and instance.email:
        BillingProfile.objects.get_or_create(user=instance, email=instance.email)


post_save.connect(user_created_receiver, sender=User)

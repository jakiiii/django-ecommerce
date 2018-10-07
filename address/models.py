from django.db import models

from billing.models import BillingProfile

ADDRESS_TYPE = (
    ('', '--- --- ---'),
    ('billing', 'Billing'),
    ('shipping', 'Shipping'),
)


# Create your manager here.
class AddressManager(models.Manager):
    pass


# Create your models here.
class Address(models.Model):
    billing_profile = models.ForeignKey(BillingProfile, on_delete=models.CASCADE)
    address_type = models.CharField(max_length=120, choices=ADDRESS_TYPE)
    address_1 = models.CharField(max_length=120)
    address_2 = models.CharField(max_length=120, null=True, blank=True)
    country = models.CharField(max_length=120, default='Bangladesh')
    city = models.CharField(max_length=120)
    state = models.CharField(max_length=120, null=True, blank=True)
    postal_code = models.CharField(max_length=120)

    objects = AddressManager()

    def __str__(self):
        return self.billing_profile

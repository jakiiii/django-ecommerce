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
        return str(self.billing_profile)

    def get_address(self):
        return "{address1}\n{address2}\n{city}\n{state}, {postal}\n{country}".format(
            address1=self.address_1,
            address2=self.address_2 or "",
            city=self.city,
            state=self.state or "",
            postal=self.postal_code,
            country=self.country
        )

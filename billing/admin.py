from django.contrib import admin

from .models import BillingProfile
from .models import Card

# Register your models here.
admin.site.register(BillingProfile)
admin.site.register(Card)

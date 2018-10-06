from decimal import Decimal

from django.db import models
from django.contrib.auth import settings
from django.db.models.signals import pre_save, m2m_changed

from products.models import Product

USER = settings.AUTH_USER_MODEL


# Create your models here.
class CartManager(models.Manager):

    def new_or_get(self, request):
        cart_id = request.session.get("cart_id", None)
        qs = self.get_queryset().filter(id=cart_id)
        if qs.count() == 1:
            new_obj = False
            cart_obj = qs.first()
            if request.user.is_authenticated and cart_obj.user is None:
                cart_obj.user = request.user
                cart_obj.save()
        else:
            cart_obj = Cart.objects.new(user=request.user)
            new_obj = True
            request.session['cart_id'] = cart_obj.id
        return cart_obj, new_obj

    def new(self, user=None):
        user_obj = None
        if user is not None:
            if user.is_authenticated:
                user_obj = user
        return self.model.objects.create(user=user_obj)


# Create your models here.
class Cart(models.Model):
    user = models.ForeignKey(USER, on_delete=models.CASCADE, null=True, blank=True)
    products = models.ManyToManyField(Product, blank=True)
    subtotal = models.DecimalField(max_digits=50, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=50, decimal_places=2, default=0.00)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = CartManager()

    def __str__(self):
        return str(self.id)


def cart_m2m_changed_receiver(sender, instance, action, *args, **kwargs):
    if action == 'post_add' or action == 'post_remove' or action == 'post_clear':
        products = instance.products.all()
        total = 0
        for x in products:
            total += x.price
        if instance.subtotal != total:
            instance.subtotal = total
            instance.save()


def cart_pre_save_receiver(sender, instance, *args, **kwargs):
    if instance.subtotal > 0:
        instance.total = format(Decimal(instance.subtotal) * Decimal(1.08), '.2f')  # tax, shipping charge, coupon etc
    else:
        instance.total = 0.00


m2m_changed.connect(cart_m2m_changed_receiver, sender=Cart.products.through)
pre_save.connect(cart_pre_save_receiver, sender=Cart)

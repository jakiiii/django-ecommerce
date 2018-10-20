from django.conf import settings

from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from .signals import object_viewed_signals
from .utils import get_client_ip

User = settings.AUTH_USER_MODEL


# Create your models here.
class ObjectViewed(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    ip_address = models.CharField(max_length=220, null=True, blank=True)  # IP Fields
    content_type = models.ForeignKey(ContentType, on_delete=models.CharField)  # User, Product, Cart, all models
    object_id = models.PositiveIntegerField()  # user_id, product_id, cart_id
    content_object = GenericForeignKey('content_type', 'object_id')  # Product Instance
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s viewed on %s" % (self.content_type, self.timestamp)

    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Object viewed'
        verbose_name_plural = 'Objects viewed'


def object_viewed_receiver(sender, instance, request, *args, **kwargs):
    c_type = ContentType.objects.get_for_model(sender)

    new_view_object = ObjectViewed.objects.create(
        user=request.user,
        content_type=c_type,
        object_id=instance.id,
        ip_address=get_client_ip(request)
    )


object_viewed_signals.connect(object_viewed_receiver)

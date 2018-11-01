from django.db import models
from django.db.models.signals import pre_save

from ecommerce.utils import unique_slug_generator


# Create your models here.
class Tag(models.Model):
    title = models.CharField(max_length=120)
    timestamp = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    slug = models.SlugField(unique=True, blank=True)

    def __str__(self):
        return self.title

    # def get_absolute_url(self):
    #     return reverse('tag', kwargs={slug: self.slug})


def tag_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(tag_pre_save_receiver, sender=Tag)

import os
import random

from django.db import models
from django.db.models import Q
from django.core.files.storage import FileSystemStorage
from django.db.models.signals import pre_save

from tags.models import Tag

from django.urls import reverse

from ecommerce.utils import unique_slug_generator
fs = FileSystemStorage(location='media')


def get_filename_exist(file_path):
    base_name = os.path.basename(file_path)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_image_path(inistance, file_name):
    new_filename = random.randint(1, 101119)
    name, ext = get_filename_exist(file_name)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename, ext=ext)
    return "products/{new_filename}/{final_filename}".format(new_filename=new_filename, final_filename=final_filename)


# Create your queryset here.
class ProductQuerySet(models.query.QuerySet):
    def featured(self):
        return self.filter(featured=True)

    def active(self):
        return self.filter(active=True)

    def search(self, query):
        lookups = (
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(price__icontains=query) |
                Q(tags__title__icontains=query)
        )
        return self.active().filter(lookups).distinct()


# Create your model manager here.
class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db)

    def all(self):
        return self.get_queryset().active()

    def featured(self):
        return self.get_queryset().featured()

    def get_by_id(self, id):
        qs = self.get_queryset().filter(id=id)
        if qs.count() == 1:
            return qs.first()
        return qs

    def search(self, query):
        return self.get_queryset().search(query)


# Create your models here.
class Product(models.Model):
    title = models.CharField(max_length=120)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    description = models.TextField(null=True, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    image = models.ImageField(upload_to=upload_image_path, null=True, blank=True)
    featured = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    slug = models.SlugField(blank=True, unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = ProductManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        # return "/products/{slug}".format(slug=self.slug)
        return reverse("product-detail", kwargs={"slug": self.slug})


def product_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(product_pre_save_receiver, sender=Product)

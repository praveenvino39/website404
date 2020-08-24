from django.db import models
import datetime
from django.contrib.auth.models import User

# Create your models here.


class Product(models.Model):
    slug = models.SlugField(default=100, unique=True)
    title = models.CharField(max_length=200, primary_key=True)
    description = models.TextField(blank=True)
    price = models.IntegerField(default=0)
    featured = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)
    color = models.CharField(null=True,max_length=10)
    mockup = models.CharField(max_length=200)
    design = models.CharField(max_length=200)

    def __str__(self):
        return self.title

class ProductImage(models.Model):
    title = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    mockup = models.ImageField(upload_to='product/image')
    design = models.ImageField(upload_to='product/image')

    def __str__(self):
        return str(self.title)


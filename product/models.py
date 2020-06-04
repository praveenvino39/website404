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
    color1 = models.CharField(blank=True, max_length=10)
    color2 = models.CharField(blank=True, max_length=10)
    color3 = models.CharField(blank=True, max_length=10)

    def __str__(self):
        return self.title

class ProductImage(models.Model):
    title = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    main = models.ImageField(upload_to='product/image')
    color1 = models.ImageField(blank=True,  upload_to='product/image')
    color2 = models.ImageField(blank=True, upload_to='product/image')
    color3 = models.ImageField(blank=True, upload_to='product/image')
    back = models.ImageField(upload_to='product/image')
    chart = models.ImageField(upload_to='product/image')

    def __str__(self):
        return str(self.title)


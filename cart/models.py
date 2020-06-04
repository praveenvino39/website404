from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Cartitem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='cart')
    title = models.CharField(max_length=300)
    color = models.CharField(max_length=20)
    size = models.CharField(max_length=10)
    quantity = models.IntegerField()
    price = models.IntegerField()

    def __str__(self):
        return self.title
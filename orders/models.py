from django.db import models
from cart.models import Cartitem
# Create your models here.


class OrderId(models.Model):
    order_id = models.IntegerField(primary_key=True)
    order_status = models.CharField(default='Initiated', blank=False, max_length=100)
    payment_status = models.CharField(default='Initiated', blank=False , max_length=100)

    def __str__(self):
        return str(self.order_id)


class ShippingDetail(models.Model):
    order_id = models.ForeignKey(OrderId, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    zipcode = models.IntegerField()
    state = models.CharField(max_length=200)
    email = models.EmailField()
    phone_number = models.BigIntegerField() 
    address = models.TextField()
    note = models.TextField()

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)



class Order(models.Model):
    order_id = models.ForeignKey(OrderId, on_delete=models.CASCADE)
    title = models.CharField(max_length=300)
    quantity = models.IntegerField()
    size = models.CharField(max_length=10)
    color = models.CharField(max_length=20)

    def __str__(self):
        return self.title


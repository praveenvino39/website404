from django.contrib import admin
from .models import OrderId, ShippingDetail, Order
# Register your models here.


class OrderIdAdmin(admin.ModelAdmin):
    search_fields = ['order_id']


class OrderAdmin(admin.ModelAdmin):
    search_fields = ['order_id__order_id']


class ShippingDetailAdmin(admin.ModelAdmin):
    search_fields = ['order_id__order_id']


admin.site.register(OrderId, OrderIdAdmin)
admin.site.register(ShippingDetail, ShippingDetailAdmin)
admin.site.register(Order, OrderAdmin)


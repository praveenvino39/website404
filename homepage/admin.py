from django.contrib import admin
from .models import ContactMessage, Subscriber
# Register your models here.

admin.site.register(ContactMessage)
admin.site.register(Subscriber)
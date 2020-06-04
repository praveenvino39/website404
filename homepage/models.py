from django.db import models

# Create your models here.


class ContactMessage(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=300)
    message = models.TextField()

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)

class Subscriber(models.Model):
    email = models.EmailField()

    def __str__(self):
        return str(self.email)

# Generated by Django 3.0.6 on 2020-05-29 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0006_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='featured',
            field=models.BooleanField(default=False),
        ),
        migrations.DeleteModel(
            name='Order',
        ),
    ]

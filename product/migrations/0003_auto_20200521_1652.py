# Generated by Django 3.0.6 on 2020-05-21 16:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_auto_20200521_0952'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productimage',
            name='title',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='product.Product'),
        ),
    ]
# Generated by Django 3.0.6 on 2020-08-23 08:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0012_auto_20200823_0509'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='design',
            field=models.ImageField(null=True, upload_to='product/image'),
        ),
        migrations.AddField(
            model_name='product',
            name='mockup',
            field=models.ImageField(null=True, upload_to='product/image'),
        ),
        migrations.AlterField(
            model_name='product',
            name='color1',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
# Generated by Django 3.0.6 on 2020-08-23 05:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0011_auto_20200822_1844'),
    ]

    operations = [
        migrations.RenameField(
            model_name='productimage',
            old_name='back',
            new_name='design',
        ),
        migrations.RenameField(
            model_name='productimage',
            old_name='chart',
            new_name='mockup',
        ),
        migrations.RemoveField(
            model_name='product',
            name='color2',
        ),
        migrations.RemoveField(
            model_name='product',
            name='color3',
        ),
        migrations.RemoveField(
            model_name='productimage',
            name='color1',
        ),
        migrations.RemoveField(
            model_name='productimage',
            name='color2',
        ),
        migrations.RemoveField(
            model_name='productimage',
            name='color3',
        ),
        migrations.RemoveField(
            model_name='productimage',
            name='main',
        ),
    ]
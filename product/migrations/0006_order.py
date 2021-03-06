# Generated by Django 3.0.6 on 2020-05-26 08:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('product', '0005_auto_20200521_2053'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('productcode', models.CharField(max_length=200)),
                ('size', models.CharField(max_length=10)),
                ('color', models.CharField(max_length=10)),
                ('name', models.CharField(max_length=200)),
                ('address', models.TextField()),
                ('pincode', models.CharField(max_length=10)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

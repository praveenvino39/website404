from rest_framework import serializers
from .models import Product, ProductImage


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Product
        fields = ['title', 'description', 'color', 'price', 'featured', 'slug', 'mockup', 'design']
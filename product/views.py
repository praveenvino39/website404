from django.shortcuts import render, redirect, get_object_or_404
from .models import ProductImage, Product
from datetime import date
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import ProductSerializer

from django.http import HttpResponse
# Create your views here.


def allproduct(request):
    products = Product.objects.all()
    return render(request, 'product/allproduct.html', {'products': products})

def showproduct(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'product/showproduct.html', {'product':product})

def checkout(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request,'product/checkoutpage.html',  {'product':product})

@api_view(['GET'])
def shopApi(request):
    products = Product.objects.all()
    products = ProductSerializer(products,context={'request': request}, many=True)
    return Response(products.data)




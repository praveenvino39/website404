from django.shortcuts import render, redirect
from product.models import Product
from .models import ContactMessage, Subscriber
from django.contrib import messages
from django.http import HttpResponse

# Create your views here.


def homepage(request):
    # products = Product.objects.all()
    products = Product.objects.filter(featured=True)
    return render(request, 'homepage/homepage.html', {'products': products})


def contact(request):
    if request.method == 'POST':
        message = ContactMessage(first_name = request.POST.get('c_fname') , last_name = request.POST.get('c_lname') , email = request.POST.get('c_email') , subject = request.POST.get('c_subject') , message = request.POST.get('c_message'))
        message.save()
        messages.success(request, 'Your message sent successfully, We\'ll responed you soon!')
        return redirect('homepage')
    return render(request, 'homepage/contact.html')


def about(request):
    return render(request, 'homepage/about.html')

def subscriber(request):
    if request.method == 'POST':
        new_sub = Subscriber(email=request.POST.get('email'))
        new_sub.save()
        return render(request, 'homepage/subscribethankyou.html')


def shop(request):
    products = Product.objects.all().order_by('-date')
    return render(request, 'homepage/shop.html', {'products': products, 'current':'New - Old'})


def featured(request):
    products = Product.objects.filter(featured = True)
    return render(request, 'homepage/shop.html', {'products': products, 'current': 'Featured'})


def shopold(request):
    return render(request, 'homepage/shop.html', {'products':Product.objects.all().order_by('date'), 'current':'Old - New'})


def high(request):
    return render(request, 'homepage/shop.html',
                  {'products': Product.objects.all().order_by('-price'), 'current': 'High Price - Low Price'})


def low(request):
    return render(request, 'homepage/shop.html',
                  {'products': Product.objects.all().order_by('price'), 'current': 'Low Price - High Price'})
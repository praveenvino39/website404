from django.shortcuts import render, redirect, get_object_or_404
from product.models import Product
from .models import Cartitem
from django.http import HttpResponse
from django.contrib import messages


def cart(request):
    is_empty = True
    cartitems=Cartitem.objects.filter(user=request.user)
    total = 0
    if len(cartitems) > 0:
        is_empty = False
        for item in cartitems:
            if item.quantity > 1:
                price = item.price * item.quantity
                total += price
            else:
                total += item.price
    else:
        is_empty = True
    return render(request, 'cart/cartview.html', {'cartitems': cartitems, 'is_empty': is_empty, 'total':total})

def removeitem(request, id):
    cart = get_object_or_404(Cartitem, pk=id)
    cart.delete()
    return redirect('cart')

def addtocart(request, slug):
    if request.method == 'POST':
        if request.POST['btn'] == 'addtocart':
            if request.POST.get('size') == 'none' or request.POST.get('color') == 'none':
                messages.error(request, 'Choose your size and color.', extra_tags='danger')
                return redirect('showproduct', slug)
            product = get_object_or_404(Product, slug=slug)
            newitem = Cartitem(user=request.user, title=product.title, size=request.POST.get('size'), color=request.POST.get('color'), quantity=request.POST['quantity'], price=product.price)
            newitem.save()
            messages.success(request, 'Item Added to Cart.')
            return redirect('homepage')
        elif request.POST['btn'] == 'buynow':
            print('Buy Now')
            return HttpResponse('Guest Checkout')


def updateitem(request):
    if request.method == 'POST':
        print('POST calling')
        if request.POST['btn'] == 'minus':
            print('minus')
            return HttpResponse('minus clicked')
        elif request.POST['btn'] == 'plus':
            print('plus')
            return HttpResponse('Plus clicked')
    else:
        print('get calling')
        # return redirect('cart')
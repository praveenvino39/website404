from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.safestring import mark_safe
from product.models import Product
from .models import Cartitem
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required


@login_required
def cart(request):
    is_empty = True
    cartitems = Cartitem.objects.filter(user=request.user)
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
    return render(request, 'cart/cartview.html', {'cartitems': cartitems, 'is_empty': is_empty, 'total': total})


@login_required
def removeitem(request, id):
    cart = get_object_or_404(Cartitem, pk=id)
    cart.delete()
    return redirect('cart')


def addtocart(request, slug):
    if request.method == 'POST':
        if request.POST['btn'] == 'addtocart':
            return addtocartfunction(request, slug)
        elif request.POST['btn'] == 'buynow':
            if request.POST.get('size') == 'none':
                messages.error(request, 'Choose your size and color.', extra_tags='danger')
                return redirect('showproduct', slug)
            print('Buy Now')
            product = get_object_or_404(Product, slug=slug)
            size = request.POST.get('size')
            color = request.POST.get('color')
            quantity = request.POST.get('quantity')
            total = product.price * quantity
            return render(request, 'orders/checkoutguest.html',
                          {'product': product, 'size': size, 'color': color, 'quantity': quantity,
                           'total': product.price})
    else:
        return redirect('homepage')        


@login_required
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


@login_required()
def addtocartfunction(request, slug):
    if request.POST.get('size') == 'none' or request.POST.get('color') == 'none':
        messages.error(request, 'Choose your size and color.', extra_tags='danger')
        return redirect('showproduct', slug)
    product = get_object_or_404(Product, slug=slug)
    newitem = Cartitem(user=request.user, title=product.title, size=request.POST.get('size'),
                       color=request.POST.get('color'), quantity=request.POST.get('quantity'), price=product.price)
    newitem.save()
    messages.success(request, mark_safe('Item added to cart  <b><a href="\cart">View Cart</a></b>'))
    return redirect('homepage')

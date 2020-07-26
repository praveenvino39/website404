from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from cart.models import Cartitem
from product.models import Product
from django.contrib import messages
from orders.models import OrderId, ShippingDetail, Order
import random
import os
from . import Checksum
# Create your views here.


def checkout(request):
    items = Cartitem.objects.filter(user=request.user)
    total = 0
    if len(items) > 0:
        is_empty = False
        for item in items:
            if item.quantity > 1:
                price = item.price * item.quantity
                total += price
            else:
                total += item.price
    return render(request, 'orders/checkout.html', {'items':items, 'total': total})

def processorderguest(request, slug):
    if request.method == 'POST':
        # try:
        product = get_object_or_404(Product, slug=slug)
        total = product.price*int(request.POST.get('quantity'))
        int(request.POST.get('c_postal_zip'))
        order_id = generate_order_id()
        order = OrderId(order_id=order_id, amount=total, order_status='Initiated', payment_status='Initiated')
        order.save()
        product = get_object_or_404(Product, slug=slug)
        neworder = Order(order_id=order, title=product.title, quantity=request.POST.get('quantity'), size=request.POST.get('size'), color=request.POST.get('color'))
        neworder.save()
        ship = ShippingDetail(order_id=order, first_name=request.POST.get('c_fname'),
                              last_name=request.POST.get('c_lname'),
                              zipcode=request.POST.get('c_postal_zip'),
                              state=request.POST.get('c_state_country'),
                              address='{} / {}'.format(request.POST.get('c_address'), request.POST.get('c_doorno')),
                              email=request.POST.get('c_email_address'),
                              phone_number=request.POST.get('c_phone'),
                              note=request.POST.get('c_order_notes')
                              )
        ship.save()
        paytmParams = {

            # Find your MID in your Paytm Dashboard at https://dashboard.paytm.com/next/apikeys
            "MID": 'OXSLCG19790467773500',

            # Find your WEBSITE in your Paytm Dashboard at https://dashboard.paytm.com/next/apikeys
            "WEBSITE": "WEBSTAGING",

            # Find your INDUSTRY_TYPE_ID in your Paytm Dashboard at https://dashboard.paytm.com/next/apikeys
            "INDUSTRY_TYPE_ID": "Retail",

            # WEB for website and WAP for Mobile-websites or App
            "CHANNEL_ID": "WEB",

            # Enter your unique order id
            "ORDER_ID": str(order_id),

            # unique id that belongs to your customer
            "CUST_ID": request.POST.get('c_email_address'),

            # customer's mobile number
            "MOBILE_NO": request.POST.get('c_phone'),

            # customer's email
            "EMAIL": request.POST.get('c_email_address'),

            # Amount in INR that is payble by customer
            # this should be numeric with optionally having two decimal points
            "TXN_AMOUNT": str(total),

            # on completion of transaction, we will send you the response on this URL
            "CALLBACK_URL": 'http://127.0.0.1:8000/order/verify-payment',
        }

        # Generate checksum for parameters we have
        # Find your Merchant Key in your Paytm Dashboard at https://dashboard.paytm.com/next/apikeys
        checksum = Checksum.generate_checksum(paytmParams, 'xjTU8MaFEEF@n61p')

        # for Staging
        url = "https://securegw-stage.paytm.in/order/process"
        return render(request, 'orders/processpayment.html', {'paytmParams': paytmParams, 'checksum': checksum, 'url': url})
        # except ValueError:
        #     messages.error(request, 'Invalid Pincode', extra_tags='danger')
        #     return redirect('checkout')


def processorder(request):
    if request.method == 'POST':
        # try:
        items = Cartitem.objects.filter(user=request.user)
        total = 0
        if len(items) > 0:
            for item in items:
                if item.quantity > 1:
                    price = item.price * item.quantity
                    total += price
                else:
                    total += item.price
        int(request.POST.get('c_postal_zip'))
        order_id = generate_order_id()
        order = OrderId(order_id=order_id, amount=total, order_status='Initiated', payment_status='Initiated')
        order.save()
        ship = ShippingDetail(order_id=order, first_name=request.POST.get('c_fname'),
                              last_name=request.POST.get('c_lname'),
                              zipcode=request.POST.get('c_postal_zip'),
                              state=request.POST.get('c_state_country'),
                              address='{} / {}'.format(request.POST.get('c_address'), request.POST.get('c_doorno')),
                              email=request.POST.get('c_email_address'),
                              phone_number=request.POST.get('c_phone'),
                              note=request.POST.get('c_order_notes')
                              )
        ship.save()
        cartitems=Cartitem.objects.filter(user=request.user)
        for item in cartitems:
            neworder=Order(order_id=order, title=item.title, quantity=item.quantity,size=item.size,color=item.color)
            neworder.save()
        if request.POST.get('paymentmode') == 'online':
            paytmParams = {

                # Find your MID in your Paytm Dashboard at https://dashboard.paytm.com/next/apikeys
                "MID": os.environ.get('MID'),

                # Find your WEBSITE in your Paytm Dashboard at https://dashboard.paytm.com/next/apikeys
                "WEBSITE": "WEBSTAGING",

                # Find your INDUSTRY_TYPE_ID in your Paytm Dashboard at https://dashboard.paytm.com/next/apikeys
                "INDUSTRY_TYPE_ID": "Retail",

                # WEB for website and WAP for Mobile-websites or App
                "CHANNEL_ID": "WEB",

                # Enter your unique order id
                "ORDER_ID": str(order_id),

                # unique id that belongs to your customer
                "CUST_ID": request.POST.get('c_email_address'),

                # customer's mobile number
                "MOBILE_NO": request.POST.get('c_phone'),

                # customer's email
                "EMAIL": request.POST.get('c_email_address'),

                # Amount in INR that is payble by customer
                # this should be numeric with optionally having two decimal points
                "TXN_AMOUNT": str(total),

                # on completion of transaction, we will send you the response on this URL
                "CALLBACK_URL": 'https://shopno404.herokuapp.com/order/verify-payment/',
            }

            # Generate checksum for parameters we have
            # Find your Merchant Key in your Paytm Dashboard at https://dashboard.paytm.com/next/apikeys
            checksum = Checksum.generate_checksum(paytmParams, os.environ.get('KEY'))

            # for Staging
            url = "https://securegw-stage.paytm.in/order/process"
            return render(request, 'orders/processpayment.html', {'paytmParams': paytmParams, 'checksum': checksum, 'url': url})
        elif request.POST.get('paymentmode') == 'cod':
            responsecode = '01'
            reponsemessage = 'Your order successfully placed'
            updateorder = get_object_or_404(OrderId, order_id=order_id)
            updateorder.order_status = 'ordered'
            updateorder.payment_status = 'COD order'
            updateorder.save()
            return render(request, 'orders/paymentstatus.html',
                          {'reponsemessage': reponsemessage, 'responsecode': responsecode, 'orderid': order_id})


@csrf_exempt
def verifypayment(request):
    if request.method == 'POST':
        response = {
            "MID": request.POST.get('MID'),
            "TXNID": request.POST.get('TXNID'),
            "ORDERID": request.POST.get('ORDERID'),
            "BANKTXNID": request.POST.get('BANKTXNID'),
            "TXNAMOUNT": request.POST.get('TXNAMOUNT'),
            "CURRENCY": request.POST.get('CURRENCY'),
            "STATUS": request.POST.get('STATUS'),
            "RESPCODE": request.POST.get('RESPCODE'),
            "RESPMSG": request.POST.get('RESPMSG'),
            "TXNDATE": request.POST.get('TXNDATE'),
            "GATEWAYNAME": request.POST.get('GATEWAYNAME'),
            "BANKNAME": request.POST.get('BANKNAME'),
            "PAYMENTMODE": request.POST.get('PAYMENTMODE'),
            "CHECKSUMHASH": request.POST.get('CHECKSUMHASH')
        }
        return render(request, 'orders/verifypayment.html', {'response':response})

@csrf_exempt
def paymentstatus(request):
    if request.method == 'POST':
        reponsemessage = ''
        responsecode = request.POST.get('RESPCODE')
        if request.POST.get('RESPCODE') == '01':
            reponsemessage = 'Your order successfully placed'.format(request.POST.get('ORDERID'))
            try:
                cart = Cartitem.objects.filter(user=request.user)
                for item in cart:
                    item.delete()
            except:
                pass
        else:
            reponsemessage = 'Some thing went wrong try again.'
        updateorder = get_object_or_404(OrderId, order_id=request.POST.get('ORDERID'))
        updateorder.payment_status = 'Completed and Paid'
        updateorder.order_status = 'ordered'
        updateorder.save()
    return render(request, 'orders/paymentstatus.html', {'reponsemessage':reponsemessage, 'responsecode':responsecode, 'orderid':request.POST.get('ORDERID')})


def trackorder(request):
    if request.method == 'POST':
        try:
            orderid = int(request.POST.get('trackingid'))
            order = OrderId.objects.filter(order_id=orderid).first()
            status = order.order_status
            return render(request, 'orders/tracking.html', {'status': status})
        except:
            messages.error(request, 'Please enter valid tracking number', extra_tags='danger')
            return render(request, 'orders/tracking.html')
    return render(request, 'orders/tracking.html')


def generate_order_id():
    return random.randint(000000, 999999)

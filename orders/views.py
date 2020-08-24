from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import json
import requests
from cart.models import Cartitem
from product.models import Product
from django.contrib import messages
from orders.models import OrderId, ShippingDetail, Order
import random
from django.http import JsonResponse
import os
from paytmchecksum import PaytmChecksum
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
        product = get_object_or_404(Product, slug=slug)
        total = product.price*int(request.POST.get('quantity'))
        int(request.POST.get('c_postal_zip'))
        order_id = generate_order_id()
        order = OrderId(order_id=order_id, amount=total, order_status='Initiated', payment_status='Initiated')
        order.save()
        product = get_object_or_404(Product, slug=slug)
        neworder = Order(order_id=order, title=product.title, quantity=request.POST.get('quantity'), size=request.POST.get('size'), color=request.POST.get('color'))
        neworder.save()
        request.session['email'] = request.POST.get('c_email_address')
        request.session['order_id'] = order_id
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
        if request.POST.get('paymentmode') == 'online':
            paytmParams = dict()

            paytmParams["body"] = {
                "requestType": "Payment",
                "mid": "nzZtLZ85936435132832",
                "websiteName": "WEBSTAGING",
                "orderId": str(order_id),
                "callbackUrl": "https://casefactory.herokuapp.com/order/verify-payment",
                "txnAmount": {
                    "value": str(total),
                    "currency": "INR",
                },
                "userInfo": {
                    "custId": request.POST.get('c_fname') ,
                },
            }

            # Generate checksum by parameters we have in body
            # Find your Merchant Key in your Paytm Dashboard at https://dashboard.paytm.com/next/apikeys
            checksum = PaytmChecksum.generateSignature(json.dumps(paytmParams["body"]), "Q0T5qByoUdSgB9@_")

            paytmParams["head"] = {
                "signature": checksum
            }

            post_data = json.dumps(paytmParams)

            # for Staging
            url = "https://securegw.paytm.in/theia/api/v1/initiateTransaction?mid={}&orderId={}".format('nzZtLZ85936435132832', order_id)

            # for Production
            # url = "https://securegw.paytm.in/theia/api/v1/initiateTransaction?mid=YOUR_MID_HERE&orderId=ORDERID_98765"
            response = requests.post(url, data=post_data, headers={"Content-type": "application/json"}).json()
            print(response)
            return render(request, 'orders/processpayment.html',{'order_id': order_id, 'token': response['body']['txnToken']})
            # except ValueError:
            #     messages.error(request, 'Invalid Pincode', extra_tags='danger')
            #     return redirect('checkout')
        elif request.POST.get('paymentmode') == 'cod':
            responsecode = '01'
            reponsemessage = 'Your order successfully placed'
            updateorder = get_object_or_404(OrderId, order_id=order_id)
            updateorder.order_status = 'ordered'
            updateorder.payment_status = 'COD order'
            updateorder.save()
            sendit(request.POST.get('c_email_address'), order_id)
            return render(request, 'orders/paymentstatus.html',
                          {'reponsemessage': reponsemessage, 'responsecode': responsecode, 'orderid': order_id})


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
        request.session['email'] = request.POST.get('c_email_address')
        request.session['order_id'] = order_id
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
            paytmParams = dict()

            paytmParams["body"] = {
                "requestType": "Payment",
                "mid": "nzZtLZ85936435132832",
                "websiteName": "WEBSTAGING",
                "orderId": str(order_id),
                "callbackUrl": "https://casefactory.herokuapp.com/order/verify-payment",
                "txnAmount": {
                    "value": '1.00',
                    "currency": "INR",
                },
                "userInfo": {
                    "custId": request.POST.get('c_fname'),
                },
            }

            # Generate checksum by parameters we have in body
            # Find your Merchant Key in your Paytm Dashboard at https://dashboard.paytm.com/next/apikeys
            checksum = PaytmChecksum.generateSignature(json.dumps(paytmParams["body"]), "Q0T5qByoUdSgB9@_")

            paytmParams["head"] = {
                "signature": checksum
            }

            post_data = json.dumps(paytmParams)

            # for Staging
            url = "https://securegw.paytm.in/theia/api/v1/initiateTransaction?mid={}&orderId={}".format('nzZtLZ85936435132832', order_id)

            # for Production
            # url = "https://securegw.paytm.in/theia/api/v1/initiateTransaction?mid=YOUR_MID_HERE&orderId=ORDERID_98765"
            response = requests.post(url, data=post_data, headers={"Content-type": "application/json"}).json()
            return render(request, 'orders/processpayment.html', {'order_id': order_id, 'token': response['body']['txnToken']})
        elif request.POST.get('paymentmode') == 'cod':
            responsecode = '01'
            reponsemessage = 'Your order successfully placed'
            updateorder = get_object_or_404(OrderId, order_id=order_id)
            updateorder.order_status = 'ordered'
            updateorder.payment_status = 'COD order'
            updateorder.save()
            sendit(request.POST.get('c_email_address'), order_id)
            cart = Cartitem.objects.filter(user=request.user)
            for item in cart:
                item.delete()
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
            sendit(request.session['email'], request.session['order_id'])
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


def sendit(mail, order_id):
    message = Mail(
        from_email='praveena4e@gmail.com',
        to_emails=mail,
        subject='Case Factory - Order Confirmed',
        html_content="""
        <body style='margin: 0 !important; padding: 0 !important; background-color: #eeeeee;' bgcolor='#eeeeee'>
    <table border='0' cellpadding='0' cellspacing='0' width='100%'>
        <tr>
            <td align='center' style='background-color: #eeeeee;' bgcolor='#eeeeee'>
                <table align='center' border='0' cellpadding='0' cellspacing='0' width='100%' style='max-width:600px;'>
                    <tr>
                        <td align='center' valign='top' style='font-size:0; padding: 35px;' bgcolor='#000000'>
                            <div style='display:inline-block; max-width:50%; min-width:100px; vertical-align:top; width:100%;'>
                                <table align='left' border='0' cellpadding='0' cellspacing='0' width='100%' style='max-width:300px;'>
                                    <tr>
                                        <td align='left' valign='top' style='font-family: Open Sans, Helvetica, Arial, sans-serif; font-size: 36px; font-weight: 800; line-height: 48px;' class='mobile-center'>
                                            <h1 style='font-size: 36px; font-weight: 800; margin: 0; color: #ffffff;'>Case Factory</h1>
                                        </td>
                                    </tr>
                                </table>
                            </div>
                            <div style='display:inline-block; max-width:50%; min-width:100px; vertical-align:top; width:100%;' class='mobile-hide'>
                                <table align='left' border='0' cellpadding='0' cellspacing='0' width='100%' style='max-width:300px;'>
                                    <tr>
                                        <td align='right' valign='top' style='font-family: Open Sans, Helvetica, Arial, sans-serif; font-size: 48px; font-weight: 400; line-height: 48px;'>
                                            <table cellspacing='0' cellpadding='0' border='0' align='right'>
                                                <tr>
                                                    <td style='font-family: Open Sans, Helvetica, Arial, sans-serif; font-size: 18px; font-weight: 400;'>
                                                        <p style='font-size: 18px; font-weight: 400; margin: 0; color: #ffffff;'><a href='http://127.0.0.1:8000' target='_blank' style='color: #ffffff; text-decoration: none;'>Shop &nbsp;</a></p>
                                                    </td>
                                                    <td style='font-family: Open Sans, Helvetica, Arial, sans-serif; font-size: 18px; font-weight: 400; line-height: 24px;'> <a href='http://127.0.0.1:8000' target='_blank' style='color: #ffffff; text-decoration: none;'><img src='https://img.icons8.com/color/48/000000/small-business.png' width='27' height='23' style='display: block; border: 0px;' /></a> </td>
                                                </tr>
                                            </table>
                                        </td>
                                    </tr>
                                </table>
                            </div>
                        </td>
                    </tr>
                    <tr>
                        <td align='center' style='padding: 35px 35px 20px 35px; background-color: #ffffff;' bgcolor='#ffffff'>
                            <table align='center' border='0' cellpadding='0' cellspacing='0' width='100%' style='max-width:600px;'>
                                <tr>
                                    <td align='center' style='font-family: Open Sans, Helvetica, Arial, sans-serif; font-size: 16px; font-weight: 400; line-height: 24px; padding-top: 25px;'> <img src='https://img.icons8.com/carbon-copy/100/000000/checked-checkbox.png' width='125' height='120' style='display: block; border: 0px;' /><br>
                                        <h2 style='font-size: 30px; font-weight: 800; line-height: 36px; color: #333333; margin: 0;'> Thank You For Your Order! </h2>
                                    </td>
                                </tr>
                                <tr>
                                    <td align='left' style='font-family: Open Sans, Helvetica, Arial, sans-serif; font-size: 16px; font-weight: 400; line-height: 24px; padding-top: 10px;'>
                                        <p style='font-size: 16px; font-weight: 400; line-height: 24px; color: #777777;'> Your order will get delivered soon. Due to COVID-19 delivery period may get longer than usual. Thank you for your co-operation. </p>
                                    </td>
                                </tr>
                                <tr>
                                    <td align='left' style='padding-top: 20px;'>
                                        <table cellspacing='0' cellpadding='0' border='0' width='100%'>
                                            <tr>
                                                <td width='75%' align='left' bgcolor='#eeeeee' style='font-family: Open Sans, Helvetica, Arial, sans-serif; font-size: 16px; font-weight: 800; line-height: 24px; padding: 10px;'> Order ID # </td>
                                                <td width='25%' align='left' bgcolor='#eeeeee' style='font-family: Open Sans, Helvetica, Arial, sans-serif; font-size: 16px; font-weight: 800; line-height: 24px; padding: 10px;'> {} </td>
                </table>
            </td>
        </tr>
    </table>
</body>        
        """.format(order_id))
    try:
        sg = SendGridAPIClient('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')
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)





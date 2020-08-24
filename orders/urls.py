from django.urls import path
from . import views

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('process-order/', views.processorder, name='processorder'),
    path('process-order-guest/<slug:slug>', views.processorderguest, name='processorderguest'),
    # path('process-checkout/', views.checkpayment, name='checkpayment'),
    path('verify-payment', views.verifypayment, name='verifypayment'),
    path('track-order', views.trackorder, name='trackorder'),
    path('payment-status', views.paymentstatus, name='paymentstatus'),
]
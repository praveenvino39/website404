from django.urls import path
from . import views

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('process-order/', views.processorder, name='processorder'),
    # path('process-checkout/', views.checkpayment, name='checkpayment'),
    path('verify-payment', views.verifypayment, name='verifypayment'),
    path('payment-status', views.paymentstatus, name='paymentstatus')
]
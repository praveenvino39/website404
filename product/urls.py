from django.urls import path
from . import views

urlpatterns = [
    path('', views.allproduct, name='allproduct'),
    path('all/api', views.shopApi, name='shopAPI'),
    path('show/<slug:slug>', views.showproduct, name='showproduct'),
    path('checkout/<slug:slug>', views.checkout, name='checkout'),
]

from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart, name='cart'),
    path('removeitem/<int:id>', views.removeitem, name='removeitem'),
    path('updateitem/<int:id>', views.updateitem, name='updateitem'),
    path('add/<slug:slug>', views.addtocart, name='add_to_cart'),

]
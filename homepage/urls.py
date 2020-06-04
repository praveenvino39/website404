from django.urls import path
from . import views
urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('contact', views.contact, name='contact'),
    path('about', views.about, name='about'),
    path('subscriber/', views.subscriber, name='subscriber'),
    path('shop/', views.shop, name='shop'),
    path('shop/old-new', views.shopold, name='shopold'),
    path('shop/high-low', views.high, name='shophigh'),
    path('shop/low-high', views.low, name='shoplow'),
    path('shop/featured', views.featured, name='featured'),
]
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.contrib.sitemaps.views import sitemap
from product.sitemaps import ProductSitemap

sitemaps ={
    'product': ProductSitemap()
}


urlpatterns = [
    path('', include('homepage.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}),
    path('admin/', admin.site.urls),
    #PRODUCT
    path('product/', include('product.urls')),
    #ALL_AUTH
    path('accounts/', include('allauth.urls')),
    # path('google/', include('login.urls')),
    #AUTH
    path('auth/', include('Auth.urls')),
    #CART
    path('cart/', include('cart.urls')),
    #ORDER
    path('order/', include('orders.urls'))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

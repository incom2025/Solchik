from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('product /', views. ProductListView.as_view(), name='product'),
]

from django.urls import path
from . import views
from django.urls import re_path as url
#from django.conf.urls import re_path 

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^ product/$', views.ProductListView.as_view(), name='product'),
    url(r'^product/(?P<pk>\d+)$', views.ProductDetailView.as_view(), name='product-detail'),
]
from django.conf.urls import include
# Додаємо URL-адреси автентифікації сайту Django (для входу, виходу з системи, керування паролями)
urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]
urlpatterns += [
    url(r'^myproduct/$', views.LoanedProductByUserListView.as_view(), name='my-booked'),
]

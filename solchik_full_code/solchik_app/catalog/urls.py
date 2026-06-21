from django.urls import path
from .views import HomePageView, ProductDetailView, OrderCreateView, ReviewCreateView, MyBookedProductsView, ThanksView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('product/<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('order/', OrderCreateView.as_view(), name='order_create'),
    path('review/', ReviewCreateView.as_view(), name='review_create'),
    path('my-products/', MyBookedProductsView.as_view(), name='my_booked'),
    path('thanks/', ThanksView.as_view(), name='thanks'),
]

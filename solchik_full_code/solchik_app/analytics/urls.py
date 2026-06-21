from django.urls import path
from .views import DashboardView, export_orders_csv

urlpatterns = [
    path('', DashboardView.as_view(), name='analytics_dashboard'),
    path('orders.csv', export_orders_csv, name='export_orders_csv'),
]

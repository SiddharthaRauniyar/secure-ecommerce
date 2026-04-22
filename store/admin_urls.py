from django.urls import path
from . import admin_views

urlpatterns = [
    path('', admin_views.admin_dashboard, name='admin_dashboard'),
    path('orders/', admin_views.admin_orders, name='admin_orders'),
    path('update-order/<int:order_id>/', admin_views.update_order_status, name='update_order_status'),
]
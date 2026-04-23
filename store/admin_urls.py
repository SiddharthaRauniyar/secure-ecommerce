from django.urls import path
from . import admin_views

urlpatterns = [
    # Dashboard
    path('', admin_views.admin_dashboard, name='admin_dashboard'),

    # Orders
    path('orders/', admin_views.admin_orders, name='admin_orders'),
    path('orders/update/<int:order_id>/', admin_views.update_order_status, name='update_order_status'),

    # 🔥 Extra (optional but good for marks)
    path('low-stock/', admin_views.low_stock_products, name='low_stock_products'),
]
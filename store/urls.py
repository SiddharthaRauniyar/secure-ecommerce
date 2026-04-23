from django.urls import path
from . import views

urlpatterns = [

    # 🏠 Home & Products
    path('', views.home, name='home'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),

    # 🔐 Authentication
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # 🛒 Cart
    path('cart/', views.cart_view, name='cart'),
path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
path('update-cart/<int:item_id>/', views.update_cart, name='update_cart'),
path('remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    # 📦 Orders
    path('checkout/', views.checkout, name='checkout'),
    path('orders/', views.order_history, name='orders'),
    path('orders/cancel/<int:order_id>/', views.cancel_order, name='cancel_order'),

    # 🔒 Demo / Protected
    path('admin-only-demo/', views.admin_only_demo, name='admin_only_demo'),
]
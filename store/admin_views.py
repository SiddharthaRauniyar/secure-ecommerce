from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models.functions import TruncDate
from django.db.models import Count, Sum, Q
import json

from .models import Category, Product, Order
from .email_utils import send_order_status_email


def staff_required(user):
    return user.is_staff


@login_required
@user_passes_test(staff_required)
def admin_dashboard(request):
    total_users = User.objects.count()
    total_products = Product.objects.count()
    total_categories = Category.objects.count()
    total_orders = Order.objects.count()

    pending_orders = Order.objects.filter(status='Pending').count()
    completed_orders = Order.objects.filter(status='Completed').count()
    cancelled_orders = Order.objects.filter(status='Cancelled').count()

    total_revenue = (
        Order.objects.filter(status='Completed')
        .aggregate(total=Sum('total_amount'))['total'] or 0
    )

    recent_orders = Order.objects.select_related('user').order_by('-created_at')[:5]
    low_stock_products = Product.objects.filter(stock_quantity__lt=5).order_by('stock_quantity')

    orders_by_day = (
        Order.objects
        .annotate(day=TruncDate('created_at'))
        .values('day')
        .annotate(total=Count('id'))
        .order_by('day')
    )

    chart_labels = [item['day'].strftime('%Y-%m-%d') for item in orders_by_day]
    chart_data = [item['total'] for item in orders_by_day]

    status_labels = ['Pending', 'Completed', 'Cancelled']
    status_data = [pending_orders, completed_orders, cancelled_orders]

    context = {
        'total_users': total_users,
        'total_products': total_products,
        'total_categories': total_categories,
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'completed_orders': completed_orders,
        'cancelled_orders': cancelled_orders,
        'total_revenue': total_revenue,
        'recent_orders': recent_orders,
        'low_stock_products': low_stock_products,
        'chart_labels': json.dumps(chart_labels),
        'chart_data': json.dumps(chart_data),
        'status_labels': json.dumps(status_labels),
        'status_data': json.dumps(status_data),
    }
    return render(request, 'store/admin_dashboard.html', context)


@login_required
@user_passes_test(staff_required)
def admin_orders(request):
    query = request.GET.get('q', '').strip()
    status = request.GET.get('status', '').strip()

    orders = Order.objects.select_related('user').order_by('-created_at')

    if query:
        orders = orders.filter(
            Q(id__icontains=query) |
            Q(user__username__icontains=query) |
            Q(customer_name__icontains=query) |
            Q(phone__icontains=query)
        )

    if status:
        orders = orders.filter(status=status)

    return render(request, 'store/admin_orders.html', {'orders': orders})


@login_required
@user_passes_test(staff_required)
def update_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        new_status = request.POST.get('status', '').strip()

        if new_status not in ['Pending', 'Completed', 'Cancelled']:
            messages.error(request, "Invalid status.")
            return redirect('admin_orders')

        order.status = new_status
        order.save()

        try:
            send_order_status_email(order.user, order)
            messages.success(request, f'Order #{order.id} updated and email sent.')
        except Exception as e:
            print("EMAIL ERROR:", e)
            messages.warning(request, f'Order #{order.id} updated, but email could not be sent.')

    return redirect('admin_orders')


@login_required
@user_passes_test(staff_required)
def low_stock_products(request):
    products = Product.objects.filter(stock_quantity__lt=5).order_by('stock_quantity', 'name')

    return render(request, 'store/admin_low_stock.html', {
        'products': products
    })
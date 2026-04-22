from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages

from .forms import RegisterForm
from .models import Product, Category, Cart, CartItem, Order, OrderItem
from .email_utils import send_order_confirmation_email


def is_admin(user):
    return user.is_staff or user.is_superuser


def home(request):
    query = request.GET.get('q')
    category_id = request.GET.get('category')

    products = Product.objects.all()
    categories = Category.objects.all()

    if query:
        products = products.filter(name__icontains=query)

    if category_id:
        products = products.filter(category_id=category_id)

    return render(request, 'store/home.html', {
        'products': products,
        'categories': categories,
    })


def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, 'store/product_detail.html', {'product': product})


def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful.')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = RegisterForm()

    return render(request, 'store/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful.')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'store/login.html')


def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('home')


@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if product.stock_quantity <= 0:
        messages.error(request, "This product is out of stock.")
        return redirect('product_detail', product_id=product.id)

    cart, created = Cart.objects.get_or_create(user=request.user)

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product
    )

    if not created:
        if cart_item.quantity + 1 > product.stock_quantity:
            messages.error(request, "Cannot add more than available stock.")
            return redirect('cart')
        cart_item.quantity += 1
    else:
        cart_item.quantity = 1

    cart_item.save()

    messages.success(request, "Item added to cart.")
    return redirect('cart')


@login_required
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = CartItem.objects.select_related('product').filter(cart=cart)

    total = sum(item.subtotal() for item in items)

    return render(request, 'store/cart.html', {
        'items': items,
        'total': total
    })


@login_required
def update_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)

    if request.method == 'POST':
        try:
            quantity = int(request.POST.get('quantity', 1))

            if quantity <= 0:
                messages.error(request, 'Quantity must be greater than 0.')
                return redirect('cart')

            if quantity > item.product.stock_quantity:
                messages.error(request, 'Requested quantity exceeds available stock.')
                return redirect('cart')

            item.quantity = quantity
            item.save()
            messages.success(request, 'Cart updated successfully.')

        except ValueError:
            messages.error(request, 'Invalid quantity.')

    return redirect('cart')


@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    item.delete()
    messages.success(request, "Item removed from cart.")
    return redirect('cart')


@login_required
def checkout(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = CartItem.objects.select_related('product').filter(cart=cart)

    if not items.exists():
        messages.warning(request, "Your cart is empty.")
        return redirect('cart')

    total = sum(item.subtotal() for item in items)

    if request.method == 'POST':
        address = request.POST.get('address', '').strip()

        if not address:
            messages.error(request, 'Shipping address is required.')
            return redirect('checkout')

        # Stock validation before creating order
        for item in items:
            if item.quantity > item.product.stock_quantity:
                messages.error(
                    request,
                    f"Insufficient stock for {item.product.name}. Available: {item.product.stock_quantity}"
                )
                return redirect('cart')

        order = Order.objects.create(
            user=request.user,
            total_amount=total,
            shipping_address=address,
            status='Pending'
        )

        for item in items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                unit_price=item.product.price
            )

            # Reduce stock after successful order
            product = item.product
            product.stock_quantity -= item.quantity
            product.save()

        items.delete()

        try:
            send_order_confirmation_email(request.user, order)
            messages.success(request, 'Order placed successfully. Confirmation email sent.')
        except Exception as e:
            print("EMAIL ERROR:", e)
            messages.warning(request, 'Order placed successfully, but the confirmation email could not be sent.')

        return render(request, 'store/order_confirmation.html', {'order': order})

    return render(request, 'store/checkout.html', {
        'items': items,
        'total': total
    })


@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'store/orders.html', {'orders': orders})


@login_required
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    if order.status != 'Pending':
        messages.error(request, 'Only pending orders can be cancelled.')
        return redirect('orders')

    order.status = 'Cancelled'
    order.save()

    # Restore stock when order is cancelled
    order_items = OrderItem.objects.select_related('product').filter(order=order)
    for item in order_items:
        product = item.product
        product.stock_quantity += item.quantity
        product.save()

    messages.success(request, f'Order #{order.id} has been cancelled.')
    return redirect('orders')


@login_required
@user_passes_test(is_admin)
def admin_only_demo(request):
    return render(request, 'store/admin_only.html')
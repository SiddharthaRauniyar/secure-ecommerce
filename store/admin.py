from django.contrib import admin
from django.core.mail import send_mail
from .models import Category, Product, Cart, CartItem, Order, OrderItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'total_amount', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'user__email')

    def save_model(self, request, obj, form, change):
        old_status = None

        if change:
            old_obj = Order.objects.get(pk=obj.pk)
            old_status = old_obj.status

        super().save_model(request, obj, form, change)

        if change and old_status != obj.status and obj.user.email:
            send_mail(
                subject='Order Status Update - EcoSecure Shop',
                message=(
                    f'Hello {obj.user.username},\n\n'
                    f'Your order #{obj.id} status has been updated to: {obj.status}.\n\n'
                    f'Thank you for shopping with us.'
                ),
                from_email=None,
                recipient_list=[obj.user.email],
                fail_silently=True,
            )


admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(OrderItem)
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings


def send_order_confirmation_email(user, order):
    if not user.email:
        print("No email for user")
        return

    subject = f"Order Confirmation - EcoSecure Shop #{order.id}"

    context = {
        "user": user,
        "order": order,
    }

    try:
        text_content = render_to_string("store/emails/order_confirmation.txt", context)
        html_content = render_to_string("store/emails/order_confirmation.html", context)

        email = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user.email],
        )
        email.attach_alternative(html_content, "text/html")

        email.send(fail_silently=False)  # 🔥 IMPORTANT FIX

        print("Email sent successfully")

    except Exception as e:
        print("EMAIL ERROR:", e)


def send_order_status_email(user, order):
    if not user.email:
        print("No email for user")
        return

    subject = f"Order Status Update - EcoSecure Shop #{order.id}"

    context = {
        "user": user,
        "order": order,
    }

    try:
        text_content = render_to_string("store/emails/order_status.txt", context)
        html_content = render_to_string("store/emails/order_status.html", context)

        email = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user.email],
        )
        email.attach_alternative(html_content, "text/html")

        email.send(fail_silently=False)  # 🔥 IMPORTANT FIX

        print("Status email sent successfully")

    except Exception as e:
        print("EMAIL ERROR:", e)
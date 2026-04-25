from celery import shared_task
from django.core.mail import send_mail
from orders.models import Order


@shared_task
def send_order_confirmation(order_id):

    order = Order.objects.get(id=order_id)

    print("Processing order:", order_id)

    order.status = "EMAIL_SENT"
    order.save()

    send_mail(
        subject="Order Confirmation",
        message=f"Your order {order.id} is confirmed!",
        from_email="noreply@aforoo.com",
        recipient_list=["customer@example.com"],
        fail_silently=False,
    )

    print("Email sent for order:", order_id)
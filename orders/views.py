from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db import transaction

from products.models import Inventory, Store, Product
from orders.models import Order, OrderItem
from orders.tasks import send_order_confirmation  # celery


@api_view(['POST'])
def create_order(request):
    data = request.data

    store_id = data.get("store_id")
    items = data.get("items", [])

    # 1. Validate store
    try:
        store = Store.objects.get(id=store_id)
    except Store.DoesNotExist:
        return Response({"error": "Store not found"}, status=404)

    if not items:
        return Response({"error": "No items provided"}, status=400)

    with transaction.atomic():

        order = Order.objects.create(
            store=store,
            status="PENDING"
        )

        insufficient_stock = False

        for item in items:
            product_id = item.get("product_id")
            qty_requested = item.get("quantity_requested")

            try:
                inventory = Inventory.objects.select_for_update().get(
                    store=store,
                    product_id=product_id
                )
            except Inventory.DoesNotExist:
                insufficient_stock = True
                continue

            if inventory.quantity < qty_requested:
                insufficient_stock = True

            # Create order item anyway
            OrderItem.objects.create(
                order=order,
                product_id=product_id,
                quantity_requested=qty_requested
            )

        # 2. If insufficient → reject
        if insufficient_stock:
            order.status = "REJECTED"
            order.save()
            return Response({
                "order_id": order.id,
                "status": order.status,
                "message": "Insufficient stock"
            })

        # 3. If all good → deduct stock
        for item in items:
            inventory = Inventory.objects.select_for_update().get(
                store=store,
                product_id=item["product_id"]
            )
            inventory.quantity -= item["quantity_requested"]
            inventory.save()

        order.status = "CONFIRMED"
        order.save()

    # 4. Trigger Celery task
    send_order_confirmation.delay(order.id)

    return Response({
        "order_id": order.id,
        "status": order.status
    })
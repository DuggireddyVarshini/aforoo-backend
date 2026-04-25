from rest_framework.decorators import api_view
from rest_framework.response import Response

from orders.models import Order
from products.models import Inventory


@api_view(['GET'])
def store_orders(request, store_id):

    orders = Order.objects.filter(store_id=store_id).order_by('-created_at')

    data = []

    for order in orders:
        data.append({
            "order_id": order.id,
            "status": order.status,
            "created_at": order.created_at,
            "total_items": order.items.count()
        })

    return Response(data)


@api_view(['GET'])
def store_inventory(request, store_id):

    inventory = Inventory.objects.filter(store_id=store_id).select_related('product')

    data = []

    for item in inventory:
        data.append({
            "product_title": item.product.title,
            "price": item.product.price,
            "category": item.product.category.name if item.product.category else None,
            "quantity": item.quantity
        })

    return Response(sorted(data, key=lambda x: x["product_title"]))
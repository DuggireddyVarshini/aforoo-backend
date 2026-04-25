from django.db import models
from products.models import Store, Product


class Order(models.Model):
    STATUS_CHOICES = [
        ("PENDING", "PENDING"),
        ("CONFIRMED", "CONFIRMED"),
        ("REJECTED", "REJECTED"),
    ]

    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name="orders")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")
    created_at = models.DateTimeField(auto_now_add=True)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="order_items")
    quantity_requested = models.IntegerField()
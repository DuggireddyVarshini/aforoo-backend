from django.test import TestCase
from products.models import Product, Store, Inventory, Category
from orders.models import Order
from rest_framework.test import APIClient


class OrderTests(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.category = Category.objects.create(name="Electronics")

        self.store = Store.objects.create(
            name="Test Store",
            location="Hyderabad"
        )

        self.product = Product.objects.create(
            title="Phone",
            price=1000,
            category=self.category
        )

        Inventory.objects.create(
            store=self.store,
            product=self.product,
            quantity=10
        )

    def test_order_confirmed(self):
        response = self.client.post("/orders/", {
            "store_id": self.store.id,
            "items": [
                {"product_id": self.product.id, "quantity_requested": 2}
            ]
        }, format="json")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["status"], "CONFIRMED")

    def test_order_rejected(self):
        response = self.client.post("/orders/", {
            "store_id": self.store.id,
            "items": [
                {"product_id": self.product.id, "quantity_requested": 100}
            ]
        }, format="json")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["status"], "REJECTED")


class SearchTests(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.category = Category.objects.create(name="Electronics")

        Product.objects.create(
            title="Phone",
            price=1000,
            category=self.category
        )

    def test_search_products(self):
        response = self.client.get("/api/search/products/?q=phone")

        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.data["results"]) > 0)
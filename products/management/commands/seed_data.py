from django.core.management.base import BaseCommand
from faker import Faker
import random

from products.models import Category, Product, Store, Inventory


class Command(BaseCommand):
    help = "Seed database with fake data"

    def handle(self, *args, **kwargs):

        fake = Faker()

        self.stdout.write("Seeding started...")

        # -------------------
        # Categories
        # -------------------
        categories = []
        for _ in range(10):
            categories.append(
                Category.objects.create(name=fake.word())
            )

        # -------------------
        # Products
        # -------------------
        products = []
        for _ in range(1000):
            products.append(
                Product.objects.create(
                    title=fake.word() + str(random.randint(1, 10000)),
                    description=fake.text(),
                    price=random.randint(100, 50000),
                    category=random.choice(categories)
                )
            )

        # -------------------
        # Stores
        # -------------------
        stores = []
        for _ in range(20):
            stores.append(
                Store.objects.create(
                    name=fake.company(),
                    location=fake.city()
                )
            )

        # -------------------
        # Inventory
        # -------------------
        for store in stores:
            sample_products = random.sample(products, 300)

            for product in sample_products:
                Inventory.objects.create(
                    store=store,
                    product=product,
                    quantity=random.randint(1, 50)
                )

        self.stdout.write(self.style.SUCCESS("Seeding completed successfully 🚀"))
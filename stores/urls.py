from django.urls import path
from .views import store_orders, store_inventory

urlpatterns = [
    path('stores/<int:store_id>/orders/', store_orders),
    path('stores/<int:store_id>/inventory/', store_inventory),
]
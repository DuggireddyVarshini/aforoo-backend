from django.urls import path
from .views import products_list, product_detail, update_product, delete_product

urlpatterns = [
    path('products/', products_list),
    path('products/<int:pk>/', product_detail),
    path('products/<int:pk>/update/', update_product),
    path('products/<int:pk>/delete/', delete_product),
]
from django.urls import path
from .views import search_products, autocomplete_products

urlpatterns = [
    path('products/', search_products),
    path('suggest/', autocomplete_products),
]
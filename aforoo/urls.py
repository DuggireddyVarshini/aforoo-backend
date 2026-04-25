from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),   # ADD THIS
    path('orders/', include('orders.urls')),
    path('api/search/', include('search.urls')),
]
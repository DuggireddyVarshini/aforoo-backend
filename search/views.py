from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.paginator import Paginator
from django.core.cache import cache

from products.models import Product, Inventory


# =========================
# SEARCH API (WITH REDIS CACHE)
# =========================
@api_view(['GET'])
def search_products(request):

    # Cache key (includes query params like q, page, filters)
    cache_key = f"search:{request.get_full_path()}"

    # Check cache
    cached_data = cache.get(cache_key)
    if cached_data:
       print(" CACHE HIT")
       return Response(cached_data)

    products = Product.objects.all()

    q = request.GET.get('q')
    category = request.GET.get('category')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    store_id = request.GET.get('store_id')
    in_stock = request.GET.get('in_stock')
    sort = request.GET.get('sort')
    page = request.GET.get('page', 1)

    #  Filters
    if q:
        products = products.filter(title__icontains=q)

    if category:
        products = products.filter(category_id=category)

    if min_price:
        products = products.filter(price__gte=min_price)

    if max_price:
        products = products.filter(price__lte=max_price)

    if store_id and in_stock == "true":
        product_ids = Inventory.objects.filter(
            store_id=store_id,
            quantity__gt=0
        ).values_list('product_id', flat=True)

        products = products.filter(id__in=product_ids)

    # Sorting (basic)
    if sort == "price":
        products = products.order_by("price")
    else:
        products = products.order_by("-id")  # newest

    #  Pagination
    paginator = Paginator(products, 10)
    page_obj = paginator.get_page(page)

    data = []

    for p in page_obj:
        item = {
            "id": p.id,
            "title": p.title,
            "price": p.price,
            "category": p.category.name if p.category else None
        }

        # If store_id provided include quantity
        if store_id:
            try:
                inv = Inventory.objects.get(store_id=store_id, product=p)
                item["quantity"] = inv.quantity
            except Inventory.DoesNotExist:
                item["quantity"] = 0

        data.append(item)

    response_data = {
        "count": paginator.count,
        "total_pages": paginator.num_pages,
        "current_page": page_obj.number,
        "results": data
    }

    # Save to Redis cache (60 seconds)
    cache.set(cache_key, response_data, timeout=60)

    return Response(response_data)


# =========================
# AUTOCOMPLETE API (OPTIONAL CACHE)
# =========================
@api_view(['GET'])
def autocomplete_products(request):

    q = request.GET.get('q', '')

    if len(q) < 3:
        return Response({"error": "Minimum 3 characters required"}, status=400)
    #  Cache key
    cache_key = f"suggest:{q}"

    cached_data = cache.get(cache_key)
    if cached_data:
        print("CACHE HIT")
        return Response(cached_data)

    #  Prefix matches (priority)
    prefix = Product.objects.filter(title__istartswith=q)[:10]

    #  General matches
    general = Product.objects.filter(title__icontains=q).exclude(
        id__in=prefix.values_list('id', flat=True)
    )[:10]

    results = list(prefix) + list(general)

    response_data = {
        "results": [p.title for p in results[:10]]
    }

    #  Cache for 60 sec
    cache.set(cache_key, response_data, timeout=60)

    return Response(response_data)
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from products.models import Category, Product

def home_view(request):
    """
    Renders the modern storefront Home Page.
    """
    categories = Category.objects.all()[:6]
    featured_products = Product.objects.filter(is_active=True).order_by('-created_at')[:8]
    return render(request, 'home.html', {
        'categories': categories,
        'featured_products': featured_products,
    })


def product_list_view(request, category_slug=None):
    """
    Renders the Product Listing / Catalog page with Category filters, Search, Price filter & Sorting.
    """
    products = Product.objects.filter(is_active=True).select_related('category')
    current_category = None

    # Filter by category if slug is provided
    if category_slug:
        current_category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=current_category)

    # Search keyword filter
    search_query = request.GET.get('q', '').strip()
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(sku__icontains=search_query) |
            Q(category__name__icontains=search_query)
        )

    # Category dropdown filter (from GET param)
    cat_param = request.GET.get('category', '').strip()
    if cat_param and not category_slug:
        products = products.filter(category__slug=cat_param)
        current_category = Category.objects.filter(slug=cat_param).first()

    # Price range filtering
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        try:
            products = products.filter(price__gte=float(min_price))
        except ValueError:
            pass
    if max_price:
        try:
            products = products.filter(price__lte=float(max_price))
        except ValueError:
            pass

    # Sorting
    sort_option = request.GET.get('sort', '-created_at')
    valid_sorts = {
        'price_asc': 'price',
        'price_desc': '-price',
        'newest': '-created_at',
        'name_asc': 'name',
    }
    sort_field = valid_sorts.get(sort_option, '-created_at')
    products = products.order_by(sort_field)

    # Pagination: 8 or 12 items per page
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    all_categories = Category.objects.all()

    return render(request, 'products/product_list.html', {
        'page_obj': page_obj,
        'all_categories': all_categories,
        'current_category': current_category,
        'search_query': search_query,
        'sort_option': sort_option,
        'min_price': min_price or '',
        'max_price': max_price or '',
        'total_count': products.count(),
    })


def product_detail_view(request, slug):
    """
    Renders detailed information for a single product with stock info and related items.
    """
    product = get_object_or_404(Product, slug=slug, is_active=True)
    related_products = Product.objects.filter(
        category=product.category,
        is_active=True
    ).exclude(id=product.id)[:4]

    return render(request, 'products/product_detail.html', {
        'product': product,
        'related_products': related_products,
    })

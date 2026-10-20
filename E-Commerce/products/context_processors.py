def navbar_categories(request):
    """
    Context processor to make active product categories available in the navbar.
    """
    try:
        from products.models import Category
        categories = Category.objects.all()[:10]
    except Exception:
        categories = []
    return {'nav_categories': categories}

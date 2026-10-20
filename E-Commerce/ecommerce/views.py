from django.shortcuts import render

def custom_404_view(request, exception=None):
    """
    Custom 404 error page handler.
    """
    return render(request, 'errors/404.html', status=404)

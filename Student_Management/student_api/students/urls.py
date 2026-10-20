from django.urls import path, include
from rest_framework.routers import DefaultRouter    
from .views import StudentViewSet, home

router = DefaultRouter()
router.register(r'students', StudentViewSet)

urlpatterns = [
   path("",home, name="home"),
   path("api/", include(router.urls)),
]
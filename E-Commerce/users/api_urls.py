from django.urls import path
from users.api_views import (
    RegisterAPIView,
    LoginAPIView,
    LogoutAPIView,
    CurrentUserProfileAPIView,
)

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='api-register'),
    path('login/', LoginAPIView.as_view(), name='api-login'),
    path('logout/', LogoutAPIView.as_view(), name='api-logout'),
    path('profile/', CurrentUserProfileAPIView.as_view(), name='api-profile'),
]

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views as drf_token_views
from .views import (
    health,
    RegisterView,
    LoginView,
    LogoutView,
    NoteViewSet,
    CurrentUserView,
)
router = DefaultRouter()
router.register(r'notes', NoteViewSet, basename='note')

urlpatterns = [
    path('health/', health, name='Health'),

    # Auth endpoints
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('auth/user/', CurrentUserView.as_view(), name='current-user'),

    # Notes endpoints (CRUD/search)
    path('', include(router.urls)),

    # Optional: Allow DRF's session login if using browsable API
    path('auth-token/', drf_token_views.obtain_auth_token, name='drf-token-login'),
]

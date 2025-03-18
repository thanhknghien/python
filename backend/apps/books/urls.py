from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, BookViewSet

# Khởi tạo router
router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')  # Endpoint: /api/books/categories/
router.register(r'books', BookViewSet, basename='book')              # Endpoint: /api/books/books/

# Định nghĩa urlpatterns
urlpatterns = [
    path('', include(router.urls)),
]
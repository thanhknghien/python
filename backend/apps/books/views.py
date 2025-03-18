from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Category, Book
from .serializers import CategorySerializer, BookSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    @action(detail=False, methods=['get'], url_path='by-category/(?P<category_id>\d+)')
    def books_by_category(self, request, category_id=None):
        books = self.queryset.filter(CategoryID=category_id)
        serializer = self.get_serializer(books, many=True)
        return Response(serializer.data)
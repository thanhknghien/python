from rest_framework import serializers
from .models import Category, Book

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['CategoryID', 'Name']

class BookSerializer(serializers.ModelSerializer):
    CategoryID = CategorySerializer(read_only=True)

    class Meta:
        model = Book
        fields = ['BookID', 'Title', 'Author', 'Genre', 'Price', 'StockQuantity', 'CategoryID', 'ImagePath', 'category_id']  # Thêm 'category_id'

    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='CategoryID', write_only=True, required=False
    )
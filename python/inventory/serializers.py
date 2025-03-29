from rest_framework import serializers
from .models import PurchaseOrder, StockOut
from products.serializers import BookSerializer

class PurchaseOrderSerializer(serializers.ModelSerializer):
    book_title = serializers.CharField(source='book.title', read_only=True)
    
    class Meta:
        model = PurchaseOrder
        fields = '__all__'

class StockOutSerializer(serializers.ModelSerializer):
    book_title = serializers.CharField(source='book.title', read_only=True)
    
    class Meta:
        model = StockOut
        fields = '__all__' 
from rest_framework import serializers
from .models import Orders, OrderDetail
from apps.books.models import Book
from apps.accounts.models import Employee, Account
from apps.accounts.serializers import EmployeeSerializer, AccountSerializer
from apps.books.serializers import BookSerializer

class OrderDetailSerializer(serializers.ModelSerializer):
    BookID = BookSerializer(read_only=True)  # Hiển thị chi tiết sách

    class Meta:
        model = OrderDetail
        fields = ['OrderID', 'BookID', 'Quantity', 'UnitPrice']

    book_id = serializers.PrimaryKeyRelatedField(
        queryset=Book.objects.all(), source='BookID', write_only=True
    )

class OrderSerializer(serializers.ModelSerializer):
    EmployeeID = EmployeeSerializer(read_only=True)
    CustomerID = AccountSerializer(read_only=True)
    order_details = OrderDetailSerializer(many=True, source='orderdetail_set')

    class Meta:
        model = Orders
        fields = ['OrderID', 'EmployeeID', 'CustomerID', 'OrderDate', 'TotalAmount', 'Status', 'order_details']

    employee_id = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all(), source='EmployeeID', write_only=True, required=False
    )
    customer_id = serializers.PrimaryKeyRelatedField(
        queryset=Account.objects.all(), source='CustomerID', write_only=True
    )

    def create(self, validated_data):
        order_details_data = validated_data.pop('orderdetail_set')
        order = Orders.objects.create(**validated_data)
        for detail_data in order_details_data:
            OrderDetail.objects.create(OrderID=order, **detail_data)
        return order

    def update(self, instance, validated_data):
        order_details_data = validated_data.pop('orderdetail_set', None)
        instance = super().update(instance, validated_data)
        if order_details_data:
            instance.orderdetail_set.all().delete()  # Xóa chi tiết cũ
            for detail_data in order_details_data:
                OrderDetail.objects.create(OrderID=instance, **detail_data)
        return instance
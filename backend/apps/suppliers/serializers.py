from rest_framework import serializers
from .models import Supplier

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ['SupplierID', 'SupplierName', 'SupplierNumber', 'SupplierAddress', 'Status']

    def validate_SupplierNumber(self, value):
        # Kiểm tra định dạng số điện thoại (ví dụ)
        if not value.isdigit() or len(value) > 15:
            raise serializers.ValidationError("SupplierNumber must be a valid number with max length 15.")
        return value
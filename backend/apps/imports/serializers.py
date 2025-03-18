from rest_framework import serializers
from .models import ImportSlip, ImportSlipDetail
from apps.accounts.models import Employee
from apps.suppliers.models import Supplier
from apps.books.models import Book
from apps.accounts.serializers import EmployeeSerializer
from apps.suppliers.serializers import SupplierSerializer
from apps.books.serializers import BookSerializer

class ImportSlipDetailSerializer(serializers.ModelSerializer):
    BookID = BookSerializer(read_only=True)

    class Meta:
        model = ImportSlipDetail
        fields = ['SlipID', 'BookID', 'Quantity', 'UnitPrice']

    book_id = serializers.PrimaryKeyRelatedField(
        queryset=Book.objects.all(), source='BookID', write_only=True
    )

class ImportSlipSerializer(serializers.ModelSerializer):
    SupplierID = SupplierSerializer(read_only=True)
    EmployeeID = EmployeeSerializer(read_only=True)
    import_details = ImportSlipDetailSerializer(many=True, source='importslipdetail_set')

    class Meta:
        model = ImportSlip
        fields = ['SlipID', 'SupplierID', 'EmployeeID', 'ImportDate', 'TotalAmount', 'import_details']

    supplier_id = serializers.PrimaryKeyRelatedField(
        queryset=Supplier.objects.all(), source='SupplierID', write_only=True, required=False
    )
    employee_id = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all(), source='EmployeeID', write_only=True, required=False
    )

    def create(self, validated_data):
        import_details_data = validated_data.pop('importslipdetail_set')
        import_slip = ImportSlip.objects.create(**validated_data)
        for detail_data in import_details_data:
            ImportSlipDetail.objects.create(SlipID=import_slip, **detail_data)
        return import_slip

    def update(self, instance, validated_data):
        import_details_data = validated_data.pop('importslipdetail_set', None)
        instance = super().update(instance, validated_data)
        if import_details_data:
            instance.importslipdetail_set.all().delete()
            for detail_data in import_details_data:
                ImportSlipDetail.objects.create(SlipID=instance, **detail_data)
        return instance
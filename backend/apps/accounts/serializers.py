from rest_framework import serializers
from .models import Employee, Role, Permission, RolePermission, Account

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['EmployeeID', 'Status']

class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ['PermissionID', 'PermissionName']

class RoleSerializer(serializers.ModelSerializer):
    permissions = PermissionSerializer(many=True, read_only=True, source='rolepermission_set')

    class Meta:
        model = Role
        fields = ['RoleID', 'RoleName', 'permissions']

class RolePermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RolePermission
        fields = ['RoleID', 'PermissionID']

class AccountSerializer(serializers.ModelSerializer):
    RoleID = RoleSerializer(read_only=True)  # Hiển thị chi tiết vai trò
    EmployeeID = EmployeeSerializer(read_only=True)  # Hiển thị chi tiết nhân viên

    class Meta:
        model = Account
        fields = ['AccountID', 'Username', 'Password', 'FullName', 'Email', 'Phone', 'Address', 'RoleID', 'EmployeeID']
        extra_kwargs = {
            'Password': {'write_only': True}  # Không trả về password trong response
        }

    def create(self, validated_data):
        # Mã hóa password trước khi lưu
        account = Account(**validated_data)
        account.set_password(validated_data['Password'])  # Sử dụng set_password để mã hóa
        account.save()
        return account

    def update(self, instance, validated_data):
        # Cập nhật password nếu có
        if 'Password' in validated_data:
            instance.set_password(validated_data.pop('Password'))
        return super().update(instance, validated_data)
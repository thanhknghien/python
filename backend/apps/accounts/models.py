from django.db import models

class Employee(models.Model):
    EmployeeID = models.AutoField(primary_key=True)
    Status = models.CharField(max_length=20, null=False, default='Active')

    def __str__(self):
        return f"Employee {self.EmployeeID} - {self.Status}"

class Role(models.Model):
    RoleID = models.AutoField(primary_key=True)
    RoleName = models.CharField(max_length=30, null=False, unique=True)

    def __str__(self):
        return self.RoleName

class Permission(models.Model):
    PermissionID = models.AutoField(primary_key=True)
    PermissionName = models.CharField(max_length=50, null=False, unique=True)

    def __str__(self):
        return self.PermissionName

class RolePermission(models.Model):
    RoleID = models.ForeignKey(Role, on_delete=models.CASCADE)
    PermissionID = models.ForeignKey(Permission, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['RoleID', 'PermissionID'], name='unique_role_permission')
        ]

    def __str__(self):
        return f"{self.RoleID} - {self.PermissionID}"

class Account(models.Model):
    AccountID = models.AutoField(primary_key=True)
    Username = models.CharField(max_length=30, null=False, unique=True)
    Password = models.CharField(max_length=255, null=False)  # Nên mã hóa khi lưu
    FullName = models.CharField(max_length=20, null=False)
    Email = models.EmailField(max_length=50, null=False)
    Phone = models.CharField(max_length=15, null=False)
    Address = models.CharField(max_length=200, null=False)
    RoleID = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)
    EmployeeID = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.Username
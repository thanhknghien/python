from django.db import models

class Supplier(models.Model):
    SupplierID = models.AutoField(primary_key=True)
    SupplierName = models.CharField(max_length=50, null=False)
    SupplierNumber = models.CharField(max_length=15, null=False)
    SupplierAddress = models.CharField(max_length=200, null=False)
    Status = models.CharField(max_length=20, null=False, default='Active')

    def __str__(self):
        return self.SupplierName
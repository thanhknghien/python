from django.db import models
from apps.accounts.models import Employee
from apps.suppliers.models import Supplier
from apps.books.models import Book

class ImportSlip(models.Model):
    SlipID = models.AutoField(primary_key=True)
    SupplierID = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, default=None)
    EmployeeID = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)
    ImportDate = models.DateTimeField(null=False, auto_now_add=True)
    TotalAmount = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0.00)

    def __str__(self):
        return f"Slip {self.SlipID}"

class ImportSlipDetail(models.Model):
    SlipID = models.ForeignKey(ImportSlip, on_delete=models.CASCADE)
    BookID = models.ForeignKey(Book, on_delete=models.CASCADE)
    Quantity = models.IntegerField(null=False)
    UnitPrice = models.DecimalField(max_digits=10, decimal_places=2, null=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['SlipID', 'BookID'], name='unique_slip_book')
        ]

    def __str__(self):
        return f"{self.SlipID} - {self.BookID}"
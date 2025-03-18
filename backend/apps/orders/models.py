from django.db import models
from apps.accounts.models import Employee, Account
from apps.books.models import Book

class Orders(models.Model):
    OrderID = models.AutoField(primary_key=True)
    EmployeeID = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True)
    CustomerID = models.ForeignKey(Account, on_delete=models.CASCADE)
    OrderDate = models.DateTimeField(null=False, auto_now_add=True)
    TotalAmount = models.DecimalField(max_digits=10, decimal_places=2, null=False, default=0.00)
    Status = models.CharField(max_length=20, null=False, default='Pending')

    def __str__(self):
        return f"Order {self.OrderID} - {self.Status}"

class OrderDetail(models.Model):
    OrderID = models.ForeignKey(Orders, on_delete=models.CASCADE)
    BookID = models.ForeignKey(Book, on_delete=models.CASCADE)
    Quantity = models.IntegerField(null=False)
    UnitPrice = models.DecimalField(max_digits=10, decimal_places=2, null=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['OrderID', 'BookID'], name='unique_order_book')
        ]

    def __str__(self):
        return f"{self.OrderID} - {self.BookID}"
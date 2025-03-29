from django.db import models
from django.conf import settings
from products.models import Book

class PurchaseOrder(models.Model):
    order_number = models.CharField(max_length=50, unique=True)
    supplier = models.CharField(max_length=200)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"PO-{self.order_number}"

    class Meta:
        ordering = ['-created_at']

class PurchaseOrderItem(models.Model):
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE, related_name='items')
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.unit_price
        super().save(*args, **kwargs)
        # Cập nhật tổng tiền của đơn nhập
        self.purchase_order.total_amount = sum(item.total_price for item in self.purchase_order.items.all())
        self.purchase_order.save()
        # Cập nhật tồn kho
        self.book.stock += self.quantity
        self.book.save()

    def __str__(self):
        return f"{self.book.title} - {self.quantity} units"

class StockOut(models.Model):
    order_number = models.CharField(max_length=50, unique=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"SO-{self.order_number}"

    class Meta:
        ordering = ['-created_at']

class StockOutItem(models.Model):
    stock_out = models.ForeignKey(StockOut, on_delete=models.CASCADE, related_name='items')
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.unit_price
        super().save(*args, **kwargs)
        # Cập nhật tổng tiền của đơn xuất
        self.stock_out.total_amount = sum(item.total_price for item in self.stock_out.items.all())
        self.stock_out.save()
        # Cập nhật tồn kho
        if self.book.stock >= self.quantity:
            self.book.stock -= self.quantity
            self.book.save()
        else:
            raise ValueError("Không đủ sách trong kho")

    def __str__(self):
        return f"{self.book.title} - {self.quantity} units"

from django.db import models
from django.conf import settings

class SalesReport(models.Model):
    REPORT_TYPE_CHOICES = [
        ('daily', 'Báo cáo ngày'),
        ('weekly', 'Báo cáo tuần'),
        ('monthly', 'Báo cáo tháng'),
        ('yearly', 'Báo cáo năm'),
    ]

    report_type = models.CharField(max_length=20, choices=REPORT_TYPE_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()
    total_sales = models.DecimalField(max_digits=10, decimal_places=2)
    total_orders = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.get_report_type_display()} ({self.start_date} - {self.end_date})"

    class Meta:
        ordering = ['-created_at']

class InventoryReport(models.Model):
    REPORT_TYPE_CHOICES = [
        ('current', 'Báo cáo tồn kho hiện tại'),
        ('low_stock', 'Báo cáo sản phẩm sắp hết'),
        ('movement', 'Báo cáo nhập xuất'),
    ]

    report_type = models.CharField(max_length=20, choices=REPORT_TYPE_CHOICES)
    generated_at = models.DateTimeField(auto_now_add=True)
    generated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    total_products = models.IntegerField()
    total_value = models.DecimalField(max_digits=10, decimal_places=2)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.get_report_type_display()} ({self.generated_at})"

    class Meta:
        ordering = ['-generated_at']

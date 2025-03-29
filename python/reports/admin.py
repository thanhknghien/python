from django.contrib import admin
from .models import SalesReport, InventoryReport

@admin.register(SalesReport)
class SalesReportAdmin(admin.ModelAdmin):
    list_display = ('report_type', 'start_date', 'end_date', 'total_sales', 'total_orders', 'created_at')
    list_filter = ('report_type', 'created_at')
    search_fields = ('created_by__username',)
    readonly_fields = ('created_at', 'created_by', 'total_sales', 'total_orders')

@admin.register(InventoryReport)
class InventoryReportAdmin(admin.ModelAdmin):
    list_display = ('report_type', 'generated_at', 'total_products', 'total_value')
    list_filter = ('report_type', 'generated_at')
    search_fields = ('generated_by__username',)
    readonly_fields = ('generated_at', 'generated_by', 'total_products', 'total_value')

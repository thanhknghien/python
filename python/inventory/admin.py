from django.contrib import admin
from .models import PurchaseOrder, PurchaseOrderItem, StockOut, StockOutItem

@admin.register(PurchaseOrder)
class PurchaseOrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'supplier', 'created_by', 'created_at', 'total_amount')
    list_filter = ('created_at',)
    search_fields = ('order_number', 'supplier')
    readonly_fields = ('order_number', 'created_by', 'created_at', 'total_amount')

@admin.register(PurchaseOrderItem)
class PurchaseOrderItemAdmin(admin.ModelAdmin):
    list_display = ('purchase_order', 'book', 'quantity', 'unit_price', 'total_price')
    list_filter = ('purchase_order',)
    search_fields = ('book__title', 'purchase_order__order_number')

@admin.register(StockOut)
class StockOutAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'created_by', 'created_at', 'total_amount')
    list_filter = ('created_at',)
    search_fields = ('order_number',)
    readonly_fields = ('order_number', 'created_by', 'created_at', 'total_amount')

@admin.register(StockOutItem)
class StockOutItemAdmin(admin.ModelAdmin):
    list_display = ('stock_out', 'book', 'quantity', 'unit_price', 'total_price')
    list_filter = ('stock_out',)
    search_fields = ('book__title', 'stock_out__order_number')

from django.contrib import admin
from ...models import StockIn

class StockInAdmin(admin.ModelAdmin):
    def total_price(self, obj):
        return obj.price * obj.quantity
    
    total_price.short_description = 'total_price'  # Đặt tên hiển thị cho cột

    list_display = ('book', 'quantity', 'total_price', 'date', 'note')
    list_filter = ('book', 'date')
    search_fields = ('book__title',)
    ordering = ('-date',)
    fields = ('book', 'quantity', 'note','price')
    readonly_fields = ('date', 'total_price')

    def has_change_permission(self, request, obj=None):
        return False

    def has_view_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request):
        return True
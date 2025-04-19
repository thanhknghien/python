from django.contrib import admin
from ...models import StockOut

class StockOutAdmin(admin.ModelAdmin):
    def total_price(self, obj):
        return obj.book.price * obj.quantity
    
    total_price.short_description = 'Total Price'  # Đặt tên hiển thị cho cột

    list_display = ('id',  'total_price','book' ,'date', 'order_id')
    list_filter = ('book', 'date', 'order_id')
    search_fields = ('book__title',)
    ordering = ('-date',)
    fields = ('book', 'quantity','total_price' ,'note' )
    readonly_fields = ('date',)

    def has_change_permission(self, request, obj=None):
            return False

    def has_view_permission(self, request, obj=None):
        # Cho phép xem tất cả bản ghi
        return True

    def has_add_permission(self, request):
        # Cho phép tạo bản ghi mới
        return True
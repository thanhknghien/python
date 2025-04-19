from django.contrib import admin
from ...models import StockIn

class StockInAdmin(admin.ModelAdmin):
    list_display = ('book', 'quantity', 'date', 'note')
    list_filter = ('book', 'date')
    search_fields = ('book__title',)
    ordering = ('-date',)
    fields = ('book', 'quantity', 'note')
    readonly_fields = ('date',)

    def has_change_permission(self, request, obj=None):
            return False


    def has_view_permission(self, request, obj=None):
        # Cho phép xem tất cả bản ghi
        return True

    def has_add_permission(self, request):
        # Cho phép tạo bản ghi mới
        return True
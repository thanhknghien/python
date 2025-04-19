from django.contrib import admin
from ...models import StockOut

class StockOutAdmin(admin.ModelAdmin):
    def total_price(self, obj):
        return obj.book.price * obj.quantity
    
    def book_price(self, obj):
        return obj.book.price

    def order_id(self, obj):
        return obj.order.id if obj.order else None
    # order_id.short_description = 'Order ID'

    list_display = ('id', 'book', 'book_price', 'quantity', 'total_price', 'date', 'note', 'order_id')
    list_filter = ('book', 'date')
    search_fields = ('book__title', 'order__id')
    ordering = ('-date',)
    fields = ('book', 'book_price', 'quantity', 'note')
    readonly_fields = ('date', 'total_price', 'book_price')

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        # Lọc StockOut khi Order có status là "Confirmed" hoặc "Completed"
        return queryset.filter(order__status__in=['Confirmed', 'Completed']).select_related('book', 'order')

    def has_change_permission(self, request, obj=None):
        return False

    def has_view_permission(self, request, obj=None):
        return True

    def has_add_permission(self, request):
        return False  # Chặn tạo thủ công vì StockOut được tạo tự động

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['book', 'quantity', 'date', 'note', 'total_price']
        return ['date', 'total_price']

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        extra_context = extra_context or {}
        if object_id:
            extra_context['show_save'] = False
            extra_context['show_save_and_continue'] = False
            extra_context['show_delete'] = False
        return super().changeform_view(request, object_id, form_url, extra_context)
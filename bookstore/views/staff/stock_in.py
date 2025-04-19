from django.contrib import admin
from ...models import StockIn

class StockInAdmin(admin.ModelAdmin):
    list_display = ('book', 'quantity', 'date', 'note')
    list_filter = ('book', 'date')
    search_fields = ('book__title',)
    ordering = ('-date',)
    fields = ('book', 'quantity', 'note')
    readonly_fields = ('date',)

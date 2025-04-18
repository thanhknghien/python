from django.contrib import admin
from .models import User, Book, Category, Order, OrderDetail, StockIn, StockOut, Report
from .views.admin.book_admin import UserAdmin
from django.urls import path
from .views.manager.report_views import revenue_report_view

admin.site.register(User, UserAdmin)
admin.site.register(Book)
admin.site.register(Category)
admin.site.register(Order)
admin.site.register(OrderDetail)
admin.site.register(StockIn)
admin.site.register(StockOut)


class ReportAdmin(admin.ModelAdmin):
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('', revenue_report_view, name='admin_revenue_report'),
        ]
        return custom_urls + urls

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        return revenue_report_view(request)

admin.site.register(Report, ReportAdmin)
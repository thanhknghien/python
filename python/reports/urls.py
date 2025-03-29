from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'sales', views.SalesReportViewSet)
router.register(r'inventory', views.InventoryReportViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('sales/', views.sales_report, name='sales_report'),
    path('inventory/', views.inventory_report, name='inventory_report'),
] 
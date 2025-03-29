from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'purchase-orders', views.PurchaseOrderViewSet)
router.register(r'stock-outs', views.StockOutViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    # Purchase Order URLs
    path('purchase-orders/', views.purchase_order_list, name='purchase_order_list'),
    path('purchase-orders/create/', views.purchase_order_create, name='purchase_order_create'),
    path('purchase-orders/<int:pk>/', views.purchase_order_detail, name='purchase_order_detail'),
    path('purchase-orders/<int:order_pk>/items/add/', views.purchase_order_item_add, name='purchase_order_item_add'),
    
    # Stock Out URLs
    path('stock-outs/', views.stock_out_list, name='stock_out_list'),
    path('stock-outs/create/', views.stock_out_create, name='stock_out_create'),
    path('stock-outs/<int:pk>/', views.stock_out_detail, name='stock_out_detail'),
    path('stock-outs/<int:order_pk>/items/add/', views.stock_out_item_add, name='stock_out_item_add'),
] 
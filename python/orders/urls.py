from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'orders', views.OrderViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('', views.order_list, name='order_list'),
    path('create/', views.order_create, name='order_create'),
    path('<int:pk>/', views.order_detail, name='order_detail'),
    path('<int:order_pk>/items/add/', views.order_item_add, name='order_item_add'),
    path('<int:pk>/status/update/', views.order_status_update, name='order_status_update'),
] 
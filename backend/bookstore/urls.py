from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/accounts/', include('apps.accounts.urls')),
    path('api/books/', include('apps.books.urls')),
    path('api/suppliers/', include('apps.suppliers.urls')),
    path('api/orders/', include('apps.orders.urls')),
    path('api/imports/', include('apps.imports.urls')),
    path('api/promotions/', include('apps.promotions.urls')),
]

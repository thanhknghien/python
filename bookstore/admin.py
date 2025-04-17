from django.contrib import admin
from .models import Book, Category, User, StockIn, StockOut, Order, OrderDetail
# Register your models here.
admin.site.register(Book)
admin.site.register(Category)
admin.site.register(User)
admin.site.register(StockIn)
admin.site.register(StockOut)
admin.site.register(Order)
admin.site.register(OrderDetail)
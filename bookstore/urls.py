# bookstore/urls.py
from django.urls import path

from bookstore.views.manager import report_views
from .views.customer import home
from .views.customer import profile

urlpatterns = [
    path('', home.home, name='home'),
    path('books/', home.books, name='books'),
    path('profile/', profile.profile, name = 'profile'),
    path('cart/', profile.cart, name = 'cart'),

    path('api/create_order/', profile.create_order, name = 'create-order'),
    path('api/view_order/', profile.view_order, name= 'view-order'),
    path('api/search_order/', profile.search_order, name= 'search-order'),
    path('api/get_book/', profile.get_book, name = 'get-books'),

    path('manager/', report_views.home, name='revenue_report'),
    path('api/revenue/day/', report_views.revenue_by_range),
    path('api/revenue/month/', report_views.revenue_by_month),
    path('api/revenue/year/', report_views.revenue_by_year),
    path('api/statistics/revenue/', report_views.revenue_statistics),


]
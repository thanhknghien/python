# bookstore/urls.py
from django.urls import path

from bookstore.views.manager import report_views
from .views.customer import home
from .views.customer import profile


urlpatterns = [
    path('', home.home, name='home'),
    path('books/', home.books, name='books'),
    path('profile/', profile.profile, name = 'profile'),
    path('api/view_order/', profile.view_order, name= 'view-order'),

    path('manager/report/revenue/', report_views.revenue_report_view, name='revenue_report'),
    path('manager/report/inventory/', report_views.inventory_report_view, name='inventory_report'),

    # Biểu đồ
    path('chart/revenue/day/', report_views.chart_revenue_by_day, name='chart_revenue_day'),
    path('chart/revenue/month/', report_views.chart_revenue_by_month, name='chart_revenue_month'),
    path('chart/revenue/year/', report_views.chart_revenue_by_year, name='chart_revenue_year'),
    path('chart/revenue/top/', report_views.chart_top_5_revenue_products, name='chart_top_revenue'),
    path('chart/sales/best/', report_views.chart_top_5_best_sellers, name='chart_best_seller'),
    path('chart/sales/worst/', report_views.chart_top_5_worst_sellers, name='chart_worst_seller'),
    path('chart/inventory/', report_views.chart_inventory, name='chart_inventory'),

]
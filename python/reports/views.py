from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count, F
from django.utils import timezone
from datetime import timedelta
from orders.models import Order
from products.models import Book
from inventory.models import PurchaseOrder, StockOut
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models.functions import TruncDate
from .models import SalesReport, InventoryReport
from .serializers import SalesReportSerializer, InventoryReportSerializer

@login_required
def sales_report(request):
    report_type = request.GET.get('type', 'daily')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    if not start_date:
        start_date = timezone.now().date()
    if not end_date:
        end_date = timezone.now().date()
    
    orders = Order.objects.filter(
        created_at__date__range=[start_date, end_date],
        status='completed'
    )
    
    total_sales = orders.aggregate(total=Sum('total_amount'))['total'] or 0
    total_orders = orders.count()
    
    # Thống kê theo ngày
    daily_stats = orders.annotate(
        date=timezone.F('created_at__date')
    ).values('date').annotate(
        total=Sum('total_amount'),
        count=Count('id')
    ).order_by('date')
    
    context = {
        'report_type': report_type,
        'start_date': start_date,
        'end_date': end_date,
        'total_sales': total_sales,
        'total_orders': total_orders,
        'daily_stats': daily_stats
    }
    
    return render(request, 'reports/sales_report.html', context)

@login_required
def inventory_report(request):
    report_type = request.GET.get('type', 'current')
    
    if report_type == 'current':
        # Báo cáo tồn kho hiện tại
        books = Book.objects.annotate(
            total_value=F('stock') * F('price')
        ).order_by('-stock')
        
        total_products = books.count()
        total_value = books.aggregate(total=Sum('total_value'))['total'] or 0
        
        context = {
            'report_type': report_type,
            'books': books,
            'total_products': total_products,
            'total_value': total_value
        }
        
    elif report_type == 'low_stock':
        # Báo cáo sản phẩm sắp hết
        low_stock_threshold = 10
        books = Book.objects.filter(stock__lte=low_stock_threshold).order_by('stock')
        
        context = {
            'report_type': report_type,
            'books': books,
            'threshold': low_stock_threshold
        }
        
    else:  # movement
        # Báo cáo nhập xuất
        start_date = timezone.now().date() - timedelta(days=30)
        
        purchase_orders = PurchaseOrder.objects.filter(
            created_at__date__gte=start_date
        ).values('created_at__date').annotate(
            total=Sum('total_amount'),
            count=Count('id')
        ).order_by('created_at__date')
        
        stock_outs = StockOut.objects.filter(
            created_at__date__gte=start_date
        ).values('created_at__date').annotate(
            total=Sum('total_amount'),
            count=Count('id')
        ).order_by('created_at__date')
        
        context = {
            'report_type': report_type,
            'start_date': start_date,
            'purchase_orders': purchase_orders,
            'stock_outs': stock_outs
        }
    
    return render(request, 'reports/inventory_report.html', context)

class SalesReportViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SalesReport.objects.all()
    serializer_class = SalesReportSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def daily_sales(self, request):
        days = int(request.query_params.get('days', 30))
        start_date = datetime.now().date() - timedelta(days=days)
        
        daily_sales = Order.objects.filter(
            created_at__date__gte=start_date
        ).annotate(
            date=TruncDate('created_at')
        ).values('date').annotate(
            total_sales=Sum('total_amount'),
            order_count=Count('id')
        ).order_by('date')
        
        return Response(daily_sales)
    
    @action(detail=False, methods=['get'])
    def top_products(self, request):
        days = int(request.query_params.get('days', 30))
        start_date = datetime.now().date() - timedelta(days=days)
        
        top_products = Order.objects.filter(
            created_at__date__gte=start_date
        ).values(
            'items__book__title'
        ).annotate(
            total_sales=Sum('items__quantity'),
            total_revenue=Sum('items__quantity' * 'items__price')
        ).order_by('-total_revenue')[:10]
        
        return Response(top_products)

class InventoryReportViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = InventoryReport.objects.all()
    serializer_class = InventoryReportSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    @action(detail=False, methods=['get'])
    def stock_levels(self, request):
        threshold = int(request.query_params.get('threshold', 10))
        
        stock_levels = PurchaseOrder.objects.values(
            'book__title'
        ).annotate(
            total_stock=Sum('quantity')
        ).filter(
            total_stock__lte=threshold
        ).order_by('total_stock')
        
        return Response(stock_levels)
    
    @action(detail=False, methods=['get'])
    def stock_movements(self, request):
        days = int(request.query_params.get('days', 30))
        start_date = datetime.now().date() - timedelta(days=days)
        
        stock_movements = StockOut.objects.filter(
            created_at__date__gte=start_date
        ).values(
            'book__title',
            'created_at__date'
        ).annotate(
            quantity=Sum('quantity')
        ).order_by('-created_at__date')
        
        return Response(stock_movements)

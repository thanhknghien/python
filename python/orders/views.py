from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Sum
from datetime import datetime, timedelta
from .models import Order, OrderItem
from .forms import OrderForm, OrderItemForm, OrderStatusForm
from .serializers import OrderSerializer, OrderItemSerializer
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

@login_required
def order_list(request):
    search_query = request.GET.get('search', '')
    status_filter = request.GET.get('status', '')
    
    orders = Order.objects.all()
    
    if search_query:
        orders = orders.filter(
            Q(order_number__icontains=search_query) |
            Q(customer_name__icontains=search_query) |
            Q(customer_email__icontains=search_query) |
            Q(customer_phone__icontains=search_query)
        )
    
    if status_filter:
        orders = orders.filter(status=status_filter)
    
    paginator = Paginator(orders, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'orders/order_list.html', {
        'page_obj': page_obj,
        'search_query': search_query,
        'status_filter': status_filter
    })

@login_required
def order_create(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save()
            messages.success(request, 'Đơn hàng đã được tạo thành công!')
            return redirect('order_detail', pk=order.pk)
    else:
        form = OrderForm()
    return render(request, 'orders/order_form.html', {'form': form})

@login_required
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    items = order.items.all()
    status_form = OrderStatusForm(instance=order)
    return render(request, 'orders/order_detail.html', {
        'order': order,
        'items': items,
        'status_form': status_form
    })

@login_required
def order_item_add(request, order_pk):
    order = get_object_or_404(Order, pk=order_pk)
    if request.method == 'POST':
        form = OrderItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.order = order
            item.unit_price = item.book.price
            item.save()
            messages.success(request, 'Sản phẩm đã được thêm vào đơn hàng!')
            return redirect('order_detail', pk=order_pk)
    else:
        form = OrderItemForm()
    return render(request, 'orders/order_item_form.html', {
        'form': form,
        'order': order
    })

@login_required
def order_status_update(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        form = OrderStatusForm(request.POST, instance=order)
        if form.is_valid():
            new_status = form.cleaned_data['status']
            old_status = order.status
            
            # Nếu đơn hàng được xác nhận, tạo phiếu xuất kho
            if new_status == 'confirmed' and old_status == 'pending':
                from inventory.models import StockOut, StockOutItem
                stock_out = StockOut.objects.create(
                    created_by=request.user,
                    notes=f'Xuất kho cho đơn hàng #{order.order_number}'
                )
                
                for item in order.items.all():
                    StockOutItem.objects.create(
                        stock_out=stock_out,
                        book=item.book,
                        quantity=item.quantity,
                        unit_price=item.unit_price
                    )
            
            form.save()
            messages.success(request, 'Trạng thái đơn hàng đã được cập nhật!')
            return redirect('order_detail', pk=pk)
    return redirect('order_detail', pk=pk)

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = Order.objects.all()
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(customer_name__icontains=search)
        return queryset
    
    @action(detail=False, methods=['get'])
    def sales_summary(self, request):
        today = datetime.now().date()
        start_date = request.query_params.get('start_date', today - timedelta(days=30))
        end_date = request.query_params.get('end_date', today)
        
        orders = Order.objects.filter(
            created_at__date__range=[start_date, end_date]
        )
        
        total_sales = orders.aggregate(total=Sum('total_amount'))['total'] or 0
        total_orders = orders.count()
        
        return Response({
            'total_sales': total_sales,
            'total_orders': total_orders,
            'start_date': start_date,
            'end_date': end_date
        })

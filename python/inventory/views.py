from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Sum
from .models import PurchaseOrder, PurchaseOrderItem, StockOut, StockOutItem
from .forms import PurchaseOrderForm, PurchaseOrderItemForm, StockOutForm, StockOutItemForm
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import PurchaseOrderSerializer, StockOutSerializer

# Create your views here.

@login_required
def purchase_order_list(request):
    search_query = request.GET.get('search', '')
    orders = PurchaseOrder.objects.all()
    
    if search_query:
        orders = orders.filter(
            Q(order_number__icontains=search_query) |
            Q(supplier__icontains=search_query)
        )
    
    paginator = Paginator(orders, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'inventory/purchase_order_list.html', {
        'page_obj': page_obj,
        'search_query': search_query
    })

@login_required
def purchase_order_create(request):
    if request.method == 'POST':
        form = PurchaseOrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.created_by = request.user
            order.save()
            messages.success(request, 'Phiếu nhập đã được tạo thành công!')
            return redirect('purchase_order_detail', pk=order.pk)
    else:
        form = PurchaseOrderForm()
    return render(request, 'inventory/purchase_order_form.html', {'form': form})

@login_required
def purchase_order_detail(request, pk):
    order = get_object_or_404(PurchaseOrder, pk=pk)
    items = order.items.all()
    return render(request, 'inventory/purchase_order_detail.html', {
        'order': order,
        'items': items
    })

@login_required
def purchase_order_item_add(request, order_pk):
    order = get_object_or_404(PurchaseOrder, pk=order_pk)
    if request.method == 'POST':
        form = PurchaseOrderItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.purchase_order = order
            item.save()
            messages.success(request, 'Sản phẩm đã được thêm vào phiếu nhập!')
            return redirect('purchase_order_detail', pk=order_pk)
    else:
        form = PurchaseOrderItemForm()
    return render(request, 'inventory/purchase_order_item_form.html', {
        'form': form,
        'order': order
    })

@login_required
def stock_out_list(request):
    search_query = request.GET.get('search', '')
    orders = StockOut.objects.all()
    
    if search_query:
        orders = orders.filter(order_number__icontains=search_query)
    
    paginator = Paginator(orders, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'inventory/stock_out_list.html', {
        'page_obj': page_obj,
        'search_query': search_query
    })

@login_required
def stock_out_create(request):
    if request.method == 'POST':
        form = StockOutForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.created_by = request.user
            order.save()
            messages.success(request, 'Phiếu xuất đã được tạo thành công!')
            return redirect('stock_out_detail', pk=order.pk)
    else:
        form = StockOutForm()
    return render(request, 'inventory/stock_out_form.html', {'form': form})

@login_required
def stock_out_detail(request, pk):
    order = get_object_or_404(StockOut, pk=pk)
    items = order.items.all()
    return render(request, 'inventory/stock_out_detail.html', {
        'order': order,
        'items': items
    })

@login_required
def stock_out_item_add(request, order_pk):
    order = get_object_or_404(StockOut, pk=order_pk)
    if request.method == 'POST':
        form = StockOutItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.stock_out = order
            item.save()
            messages.success(request, 'Sản phẩm đã được thêm vào phiếu xuất!')
            return redirect('stock_out_detail', pk=order_pk)
    else:
        form = StockOutItemForm()
    return render(request, 'inventory/stock_out_item_form.html', {
        'form': form,
        'order': order
    })

class PurchaseOrderViewSet(viewsets.ModelViewSet):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = PurchaseOrder.objects.all()
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(book__title__icontains=search)
        return queryset
    
    @action(detail=False, methods=['get'])
    def low_stock(self, request):
        threshold = request.query_params.get('threshold', 10)
        queryset = self.get_queryset().filter(quantity__lte=threshold)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

class StockOutViewSet(viewsets.ModelViewSet):
    queryset = StockOut.objects.all()
    serializer_class = StockOutSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = StockOut.objects.all()
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(book__title__icontains=search)
        return queryset
    
    @action(detail=False, methods=['get'])
    def stock_summary(self, request):
        total_stock = PurchaseOrder.objects.aggregate(total=Sum('quantity'))['total'] or 0
        total_out = StockOut.objects.aggregate(total=Sum('quantity'))['total'] or 0
        current_stock = total_stock - total_out
        
        return Response({
            'total_stock': total_stock,
            'total_out': total_out,
            'current_stock': current_stock
        })

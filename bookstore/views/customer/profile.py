import json
from django.http import JsonResponse
from django.shortcuts import render
from ...models import Order, OrderDetail, User
from django.views.decorators.csrf import csrf_exempt

def profile(request):
    return render(request ,'customer/profile.html')

@csrf_exempt
def create_order(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            # Lấy thông tin hóa đơn và danh sách sản phẩm
            customer_name = data.get('customer_name')
            items = data.get('items', [])

            if not customer_name or not items:
                return JsonResponse({'error': 'Thiếu dữ liệu'}, status=400)

            # Tạo hóa đơn
            order = Order.objects.create(customer_name=customer_name)

            # Tạo chi tiết hóa đơn
            for item in items:
                OrderDetail.objects.create(
                    order=order,
                    product_name=item['product_name'],
                    quantity=item['quantity'],
                    price=item['price']
                )

            return JsonResponse({'message': 'Hóa đơn đã tạo', 'order_id': order.id}, status=201)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        

@csrf_exempt
def view_order(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_id = data.get('id')

            if not user_id:
                return JsonResponse({'error': 'Missing user_id'}, status=400)

            try:
                user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return JsonResponse({'error': 'User not found'}, status=404)

            orders = Order.objects.filter(user=user).order_by('-created_at')

            result = []
            for order in orders:
                order_details = OrderDetail.objects.filter(order=order).select_related('book')
                items = []
                for detail in order_details:
                    items.append({
                        'book_title': detail.book.title,
                        'quantity': detail.quantity,
                        'price': detail.price,
                        'total': detail.quantity * detail.price
                    })

                result.append({
                    'order_id': order.id,
                    'created_at': order.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                    'status': order.status,
                    'total_amount': sum(item['total'] for item in items),
                    'items': items
                })

            return JsonResponse(result, safe=False)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Method not allowed'}, status=405)


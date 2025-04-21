from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Sum, Count
from matplotlib.dates import relativedelta
from ...models import Order
from datetime import datetime, timedelta
import json
from django.utils.dateparse import parse_date
from django.db.models.functions import TruncDate, TruncYear, TruncMonth


def home(request):
    return render(request, 'manager/revenue.html')

@csrf_exempt
def revenue_by_range(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    try:
        body = json.loads(request.body)
        start_date = parse_date(body.get('start_date'))
        end_date = parse_date(body.get('end_date'))

        if not start_date or not end_date:
            return JsonResponse({'error': 'Missing start_date or end_date'}, status=400)

        # Bổ sung 1 ngày để lấy đến hết ngày end_date
        end_date_inclusive = end_date + timedelta(days=1)

        orders = Order.objects.filter(
            status='Completed',
            created_at__range=[start_date, end_date_inclusive]
        )

        total_revenue = orders.aggregate(total=Sum('total_amount'))['total'] or 0
        total_orders = orders.count()



        daily_data = orders.annotate(date=TruncDate('created_at')).values('date')\
            .annotate(total=Sum('total_amount')).order_by('date')

        chart_data = [
            {
                'date': item['date'].strftime('%Y-%m-%d'),
                'total_revenue': float(item['total'])
            }
            for item in daily_data
        ]

        return JsonResponse({
            'total_revenue': float(total_revenue),
            'total_orders': total_orders,
            'chart_data': chart_data
        })

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
@csrf_exempt
def revenue_by_month(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    try:
        body = json.loads(request.body)
        month_str = body.get('month')  # dạng 'YYYY-MM'
        if not month_str:
            return JsonResponse({'error': 'Month is required'}, status=400)

        try:
            target_date = datetime.strptime(month_str, '%Y-%m')
        except ValueError:
            return JsonResponse({'error': 'Invalid month format. Use YYYY-MM'}, status=400)

        # Xác định ngày bắt đầu và kết thúc tháng
        start_date = target_date.replace(day=1)
        # Tháng sau = tháng hiện tại + 1, ngày = 1
        if start_date.month == 12:
            end_date = start_date.replace(year=start_date.year + 1, month=1, day=1)
        else:
            end_date = start_date.replace(month=start_date.month + 1, day=1)

        result = Order.objects.filter(
            status='Completed',
            created_at__range=[start_date, end_date]
        ).aggregate(
            total_revenue=Sum('total_amount'),
            total_orders=Count('id')
        )

        total_revenue = float(result['total_revenue'] or 0)
        total_orders = result['total_orders'] or 0

        return JsonResponse({
            'month': month_str,
            'total_revenue': total_revenue,
            'total_orders': total_orders
        })

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def revenue_by_year(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    try:
        body = json.loads(request.body)
        year_str = body.get('year')  # dạng '2025'
        if not year_str:
            return JsonResponse({'error': 'Year is required'}, status=400)

        try:
            year = int(year_str)
        except ValueError:
            return JsonResponse({'error': 'Invalid year. Use YYYY format'}, status=400)

        start_date = datetime(year, 1, 1)
        end_date = datetime(year + 1, 1, 1)

        result = Order.objects.filter(
            status='Completed',
            created_at__range=[start_date, end_date]
        ).aggregate(
            total_revenue=Sum('total_amount'),
            total_orders=Count('id')
        )

        total_revenue = float(result['total_revenue'] or 0)
        total_orders = result['total_orders'] or 0

        return JsonResponse({
            'year': year,
            'total_revenue': total_revenue,
            'total_orders': total_orders
        })

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def revenue_statistics(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    try:
        data = json.loads(request.body)
        type_ = data.get('type')

        if type_ == 'day':
            start = datetime.strptime(data['start_date'], "%Y-%m-%d")
            end = datetime.strptime(data['end_date'], "%Y-%m-%d") + timedelta(days=1)
            queryset = Order.objects.filter(status="Completed", created_at__range=[start, end])
            queryset = queryset.annotate(date=TruncDate('created_at')) \
                               .values('date') \
                               .annotate(revenue=Sum('total_amount')) \
                               .order_by('date')
            labels = [str(item['date']) for item in queryset]
        elif type_ == 'month':
            start = datetime.strptime(data['start_month'], "%Y-%m")
            end = datetime.strptime(data['end_month'], "%Y-%m") + relativedelta(months=1)
            queryset = Order.objects.filter(status="Completed", created_at__range=[start, end])
            queryset = queryset.annotate(month=TruncMonth('created_at')) \
                               .values('month') \
                               .annotate(revenue=Sum('total_amount')) \
                               .order_by('month')
            labels = [item['month'].strftime("%Y-%m") for item in queryset]
        elif type_ == 'year':
            start_year = int(data['start_year'])
            end_year = int(data['end_year']) + 1
            start = datetime(start_year, 1, 1)
            end = datetime(end_year, 1, 1)
            queryset = Order.objects.filter(status="Completed", created_at__range=[start, end])
            queryset = queryset.annotate(year=TruncYear('created_at')) \
                               .values('year') \
                               .annotate(revenue=Sum('total_amount')) \
                               .order_by('year')
            labels = [item['year'].year for item in queryset]
        else:
            return JsonResponse({'error': 'Invalid type'}, status=400)

        revenues = [float(item['revenue'] or 0) for item in queryset]
        return JsonResponse({'labels': labels, 'revenues': revenues})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
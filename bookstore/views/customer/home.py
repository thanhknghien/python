# bookstore/views/customer/home.py
from django.shortcuts import render
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q
from ...models import Book, User    
from django.views.decorators.csrf import csrf_exempt
import mysql.connector

# Cấu hình kết nối MySQL
db_config = {
    'host': 'localhost',
    'user': 'root',  # Thay đổi theo cấu hình của bạn
    'password': '',  # Thay đổi theo cấu hình của bạn
    'database': 'webpython'
}

def home(request):
    return render(request, 'customer/home.html')

@csrf_exempt
def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        try:
            # Kết nối với MySQL
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor(dictionary=True)
            
            # Truy vấn kiểm tra đăng nhập
            query = "SELECT * FROM bookstore_user WHERE username = %s AND password = %s"
            cursor.execute(query, (username, password))
            user = cursor.fetchone()
            
            if user:
                # Tạo giỏ hàng mới chỉ khi đăng nhập thành công
                cursor.execute("""
                    INSERT INTO bookstore_order (user_id, address, status, total_amount)
                    VALUES (%s, '', 'Pending', 0)
                """, (user['id'],))
                cart_id = cursor.lastrowid
                conn.commit()
                
                return JsonResponse({
                    'success': True, 
                    'message': 'Đăng nhập thành công',
                    'user': {
                        'id': user['id'],
                        'username': user['username'],
                        'email': user['email'],
                        'full_name': user['full_name'],
                        'phone': user['phone'],
                        'address': user['address']
                    },
                    'cart_id': cart_id
                })
            else:
                return JsonResponse({'success': False, 'message': 'Sai tên đăng nhập hoặc mật khẩu'})
                
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
        finally:
            if 'conn' in locals():
                conn.close()
    
    return JsonResponse({'success': False, 'message': 'Method not allowed'})

@csrf_exempt
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password1')
        role="customer"
        email = request.POST.get('email')
        full_name = request.POST.get('full_name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        
        try:
            # Kết nối với MySQL
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            
            # Kiểm tra username đã tồn tại chưa
            cursor.execute("SELECT * FROM bookstore_user WHERE username = %s", (username,))
            if cursor.fetchone():
                return JsonResponse({'success': False, 'message': 'Tên đăng nhập đã tồn tại'})
            
            # Thêm user mới
            query = """
                INSERT INTO bookstore_user (username, password, email, full_name, phone, address, role)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (username, password, email, full_name, phone, address, role))
            user_id = cursor.lastrowid
            
            
            
            conn.commit()
            return JsonResponse({'success': True, 'message': 'Đăng ký thành công'})
            
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
        finally:
            if 'conn' in locals():
                conn.close()
    
    return JsonResponse({'success': False, 'message': 'Method not allowed'})

def updateItem(request):
    return JsonResponse('added', safe = False)

def books(request):
    # Lấy danh sách sách
    books = Book.objects.filter(status='available')

    # Lọc theo category nếu có
    category_id = request.GET.get('category')
    if category_id:
        books = books.filter(category_id=category_id)

    # Tìm kiếm sách
    search_query = request.GET.get('q', '')
    if search_query:
        books = books.filter(
            Q(title__icontains=search_query) |
            Q(author__icontains=search_query)
        )

    # Phân trang (10 sách mỗi trang)
    paginator = Paginator(books, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    # Chuẩn bị dữ liệu JSON
    books_data = [
        {
            'id': book.id,
            'title': book.title,
            'author': book.author,
            'price': float(book.price),
            'stock': book.stock,
            'imagePath': book.imagePath.url if book.imagePath else None,
            'description': book.description if book.description else 'Chưa có mô tả',
            'category_id': book.category.id if book.category else None,
            'category_name': book.category.name if book.category else None
        }
        for book in page_obj
    ]

    # Trả về JSON
    return JsonResponse({
        'books': books_data,
        'current_page': page_obj.number,
        'total_pages': paginator.num_pages,
        'has_previous': page_obj.has_previous(),
        'has_next': page_obj.has_next(),
        'previous_page': page_obj.previous_page_number() if page_obj.has_previous() else None,
        'next_page': page_obj.next_page_number() if page_obj.has_next() else None,
    })
def detail(request):
    id = request.GET.get('id','')
    books = Book.objects.filter(id=id)
    return render(request, 'customer/home.html', {'books': books})
@csrf_exempt
def check_login_status(request):
    if request.method == 'GET':
        try:
            # Kết nối với MySQL
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor(dictionary=True)
            
            # Lấy user_id từ session hoặc request
            user_id = request.GET.get('user_id')
            
            if user_id:
                # Kiểm tra user có tồn tại không
                cursor.execute("SELECT * FROM bookstore_user WHERE id = %s", (user_id,))
                user = cursor.fetchone()
                
                if user:
                    return JsonResponse({
                        'success': True,
                        'is_authenticated': True,
                        'user': {
                            'id': user['id'],
                            'username': user['username'],
                            'email': user['email'],
                            'full_name': user['full_name'],
                            'phone': user['phone'],
                            'address': user['address']
                        }
                    })
            
            return JsonResponse({
                'success': True,
                'is_authenticated': False
            })
                
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
        finally:
            if 'conn' in locals():
                conn.close()
    
    return JsonResponse({'success': False, 'message': 'Method not allowed'})
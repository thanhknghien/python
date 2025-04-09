import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'boms.settings')
django.setup()

from bookstore.models import User, Category, Book, Order, OrderDetail, StockIn, StockOut

def populate_sample_data():
    User.objects.all().delete()
    Category.objects.all().delete()
    Book.objects.all().delete()
    Order.objects.all().delete()
    OrderDetail.objects.all().delete()
    StockIn.objects.all().delete()
    StockOut.objects.all().delete()

    # Thêm User
    users = [
        User(username='customer1', password='pass123', full_name='Nguyen Van A', role='customer', address='123 Hanoi', email='customer1@example.com', phone='0123456789', status='active'),
        User(username='staff1', password='pass123', full_name='Tran Thi B', role='staff', address='456 HCM', email='staff1@example.com', phone='0987654321', status='active'),
    ]
    User.objects.bulk_create(users)
    print("Added Users")

    # Thêm Category
    categories = [
        Category(name='Programming'),
        Category(name='Fiction'),
    ]
    Category.objects.bulk_create(categories)
    print("Added Categories")

    # Thêm Book
    cat_programming = Category.objects.get(name='Programming')
    cat_fiction = Category.objects.get(name='Fiction')
    books = [
        Book(title='Python Crash Course', author='Eric Matthes', price=29.99, stock=50, category=cat_programming, imagePath='book_images/python.jpg', status='available', description='Python guide'),
        Book(title='The Great Gatsby', author='F. Scott Fitzgerald', price=9.99, stock=100, category=cat_fiction, imagePath='book_images/gatsby.jpg', status='available', description='Classic novel'),
    ]
    Book.objects.bulk_create(books)
    print("Added Books")

    # Thêm Order
    customer = User.objects.get(username='customer1')
    orders = [
        Order(user=customer, address='123 Hanoi', status='Pending', total_amount=39.98),
    ]
    Order.objects.bulk_create(orders)
    print("Added Orders")

    # Thêm OrderDetail
    order1 = Order.objects.get(id=1)
    book1 = Book.objects.get(title='Python Crash Course')
    book2 = Book.objects.get(title='The Great Gatsby')
    order_details = [
        OrderDetail(order=order1, book=book1, quantity=1, price=29.99),
        OrderDetail(order=order1, book=book2, quantity=1, price=9.99),
    ]
    OrderDetail.objects.bulk_create(order_details)
    print("Added OrderDetails")

    # Thêm StockIn
    stock_ins = [
        StockIn(book=book1, quantity=50, note='Initial stock'),
        StockIn(book=book2, quantity=100, note='Initial stock'),
    ]
    StockIn.objects.bulk_create(stock_ins)
    print("Added StockIns")

    # Thêm StockOut (ví dụ trống, thêm sau khi có Confirmed order)
    print("No StockOuts added yet")

if __name__ == '__main__':
    populate_sample_data()
from django.contrib import admin
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from ...models import Book, Category

"""" 
 Quản lý sản phẩm (Sách):
  Thêm sách.
  Sửa sách.
  Xóa sách.
  Xem danh sách sách.
"""

# Xem danh sách sách
@admin.register(Book)
def book_list(request):
    # Lấy tất cả và sắp xếp theo thứ tự giảm dần (-id)
    book_list = Book.objects.all().order_by('-id')

    # Tìm kiếm
    search_query = request.GET.get('search', '')
    if search_query:
        book_list = book_list.filter(title_icontains=search_query)

    # Lọc theo category
    category_id = request.GET.get('category')
    if category_id:
        book_list = book_list.filter(category_id=category_id)

    # Phân trang
    pap = Paginator(book_list, 5)
    page =  request.GET.get('page')
    books = pap.get_page(page)

    categories = Category.objects.all()

    context = {
        'book': books,
        'categories': categories,
        'search_query': search_query,
        'selected_category': category_id
    }

    return render(request, 'admin/books/book_list.html', context)

# Thêm sáchsách
@admin.register(Book)
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save()
            messages.success(request, f'Sách "{book.title}" đã được thêm thành công!')
            return redirect('admin_book_list')
    else:
        form = BookForm()

    return render(request, 'admin/books/book_form.html', {
        'form': form,
        'title': 'Thêm sách mới'
    })

# Sửa sáchsách
@admin.register(Book)
def edit_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            book = form.save()
            messages.success(request, f'Sách "{book.title}" đã được cập nhập!')
            return redirect('admin_book_list')
    else:
        form = BookForm(instance=book)

    return render(request, 'admin/books/book_form.html', {
        'form': form,
        'book': book,
        'title': 'Chỉnh sửa Sách'
    })


// static/js/customer/home.js
document.addEventListener('DOMContentLoaded', function() {
    // Kiểm tra xem có user trong localStorage không
    const user = JSON.parse(localStorage.getItem('user'));
    if (user) {
        // Nếu có user, cập nhật giao diện
        const dropdownToggle = document.querySelector('.nav-link.dropdown-toggle');
        const dropdownMenu = document.querySelector('.dropdown-menu');
        
        if (dropdownToggle && dropdownMenu) {
            dropdownToggle.innerHTML = `<i class="fas fa-user"></i> ${user.username}`;
            dropdownMenu.innerHTML = `
                <li><a class="dropdown-item" href="/profile">Thông tin cá nhân</a></li>
                <li><a class="dropdown-item" href="#" onclick="onLogout()">Đăng xuất</a></li>
            `;
        }
    }

    const searchInput = document.getElementById('search-input');
    const searchButton = document.getElementById('search-button');
    const bookList = document.getElementById('book-list');
    const pagination = document.getElementById('pagination');
    const loginForm = document.getElementById('login-form');
    const registerForm = document.getElementById('register-form');
    const allCategoryBtn = document.getElementById('all-category');
    let currentPage = 1;
    let currentQuery = '';

    // Hàm hiển thị popup đăng nhập
    window.showLoginPopup = function() {
        document.getElementById("login-popup").style.display = "block";
    }

    // Hàm ẩn popup đăng nhập
    window.hideLoginPopup = function() {
        document.getElementById("login-popup").style.display = "none";
    }

    // Hàm hiển thị popup đăng ký
    window.showRegisterPopup = function() {
        document.getElementById("register-popup").style.display = "block";
    }
    
    // Hàm ẩn popup đăng ký
    window.hideRegisterPopup = function() {
        document.getElementById("register-popup").style.display = "none";
    }
    //hàm ẩn popup detail
    window.hideDetailPopup = function () {
        detailPopup.style.display="none";
    }
    // Hàm hiển thị popup chi tiết sách
    window.showDetailPopup = function(book) {
        const detailPopup = document.getElementById("detail-popup");
        const detailContent = document.getElementById("detail-content");
        
        // Cập nhật nội dung popup
        detailContent.innerHTML = `
            <div class="row">
                <div class="col-md-4">
                    <img src="${book.imagePath || '/static/images/default_book.jpg'}" class="img-fluid" alt="${book.title}">
                </div>
                <div class="col-md-8">
                    <h3>${book.title}</h3>
                    <p><strong>Tác giả:</strong> ${book.author || 'Không rõ'}</p>
                    <p><strong>Giá:</strong> ${book.price} VNĐ</p>
                    <p><strong>Tồn kho:</strong> ${book.stock}</p>
                    <p><strong>Mô tả:</strong> ${book.description || 'Chưa có mô tả'}</p>
                    <div class="d-flex justify-content-between">
                        <button class="btn btn-success" onclick="addToCart(${book.id}, '${book.title}', ${book.price})">Thêm vào giỏ hàng</button>
                        <button class="btn btn-secondary" onclick="hideDetailPopup()">Đóng</button>
                    </div>
                </div>
            </div>
        `;
       
        // Hiển thị popup
        detailPopup.style.display = "block";
    }
    
    // Hàm ẩn popup chi tiết sách
    window.hideDetailPopup = function() {
        document.getElementById("detail-popup").style.display = "none";
    }

    // Xử lý sự kiện submit form đăng nhập
    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const formData = new FormData(loginForm);
            
            // Hiển thị loading
            const submitButton = loginForm.querySelector('button[type="submit"]');
            const originalText = submitButton.textContent;
            submitButton.textContent = 'Đang xử lý...';
            submitButton.disabled = true;
            
            fetch('/api/login/', {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                }
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                if (data.success) {
                    // Lưu thông tin người dùng vào localStorage
                    const userData = {
                        id: data.user.id,
                        username: data.user.username,
                        email: data.user.email,
                        full_name: data.user.full_name,
                        phone: data.user.phone,
                        address: data.user.address,
                        status: 'active'
                    };
                    localStorage.setItem('user', JSON.stringify(userData));
                    
                    // Tạo giỏ hàng mới nếu chưa có
                    let cart = JSON.parse(localStorage.getItem('cart'));
                    if (!cart) {
                        cart = {
                            user_id: data.user.id,
                            address: data.user.address || '',
                            cart: []
                        };
                        localStorage.setItem('cart', JSON.stringify(cart));
                    }
                    
                    location.reload();
                     
                    // Ẩn popup đăng nhập
                    hideLoginPopup();
                    
                    // Hiển thị thông báo
                    alert('Đăng nhập thành công!');
                } else {
                    alert(data.message || 'Đăng nhập thất bại');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Đã có lỗi xảy ra. Vui lòng thử lại.');
            })
            .finally(() => {
                // Khôi phục trạng thái nút
                submitButton.textContent = originalText;
                submitButton.disabled = false;
            });
        });
    }

    // Hàm đăng xuất
    window.onLogout = function() {
        // Xóa toàn bộ localStorage khi đăng xuất
        localStorage.clear();
        
        // Cập nhật giao diện
        const dropdownToggle = document.querySelector('.nav-link.dropdown-toggle');
        const dropdownMenu = document.querySelector('.dropdown-menu');
        
        if (dropdownToggle && dropdownMenu) {
            dropdownToggle.innerHTML = '<i class="fas fa-user"></i> Tài khoản';
            dropdownMenu.innerHTML = `
                <li><a class="dropdown-item" href="#" onclick="showLoginPopup()">Đăng nhập</a></li>
                <li><a class="dropdown-item" href="#" onclick="showRegisterPopup()">Đăng ký</a></li>
            `;
        }
        
        // Hiển thị thông báo
        alert('Đăng xuất thành công!');
    };

    // Xử lý sự kiện submit form đăng ký
    if (registerForm) {
        registerForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const formData = new FormData(registerForm);
            
            // Kiểm tra mật khẩu trùng khớp
            if (formData.get('password1') !== formData.get('password2')) {
                alert('Mật khẩu không trùng khớp!');
                return;
            }
            
            // Hiển thị loading
            const submitButton = registerForm.querySelector('button[type="submit"]');
            const originalText = submitButton.textContent;
            submitButton.textContent = 'Đang xử lý...';
            submitButton.disabled = true;
            
            fetch('/api/register/', {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                }
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                if (data.success) {
                    alert('Đăng ký thành công! Vui lòng đăng nhập.');
                    hideRegisterPopup();
                    showLoginPopup();
                } else {
                    alert(data.message || 'Đăng ký thất bại');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Đã có lỗi xảy ra. Vui lòng thử lại.');
            })
            .finally(() => {
                // Khôi phục trạng thái nút
                submitButton.textContent = originalText;
                submitButton.disabled = false;
            });
        });
    }

    // Hàm thêm sản phẩm vào giỏ hàng
    window.addToCart = function(bookId, title, price) {
        console.log('Thêm sách vào giỏ hàng:', { bookId, title, price });
        
        // Kiểm tra xem có user đăng nhập không
        const user = JSON.parse(localStorage.getItem('user'));
        if (!user) {
            alert('Vui lòng đăng nhập để thêm sản phẩm vào giỏ hàng!');
            showLoginPopup();
            return;
        }

        // Lấy giỏ hàng từ localStorage
        let cart = JSON.parse(localStorage.getItem('cart'));
        if (!cart) {
            cart = {
                user_id: user.id,
                address: user.address || '',
                cart: []
            };
        }

        // Kiểm tra xem sản phẩm đã có trong giỏ hàng chưa
        const existingItem = cart.cart.find(item => item.book_id === bookId);
        if (existingItem) {
            existingItem.quantity += 1;
        } else {
            cart.cart.push({
                book_id: bookId,
                quantity: 1,
                unitPrice: price
            });
        }

        // Lưu giỏ hàng vào localStorage
        localStorage.setItem('cart', JSON.stringify(cart));
        console.log('Giỏ hàng sau khi thêm:', cart);
        
        // Hiển thị thông báo
        alert('Đã thêm sản phẩm vào giỏ hàng!');
    };

    // Hàm lấy danh sách sách
    function fetchBooks(page = 1, query = '', category = '') {
        const url = `/books/?page=${page}&q=${encodeURIComponent(query)}&category=${category}`;
        fetch(url)
            .then(response => response.json())
            .then(data => {
                // Cập nhật danh sách sách
                bookList.innerHTML = '';
                if (data.books.length === 0) {
                    bookList.innerHTML = '<p>Không tìm thấy sách nào.</p>';
                } else {
                    data.books.forEach(book => {
                        bookList.innerHTML += `
                            <div class="col-md-3 book-item">
                                <div class="card">
                                    <img src="${book.imagePath || '/static/images/default_book.jpg'}" class="card-img-top" alt="${book.title}">
                                    <div class="card-body">
                                        <h5 class="card-title">${book.title}</h5>
                                        <p class="card-text">Tác giả: ${book.author || 'Không rõ'}</p>
                                        <p class="card-text">Giá: ${book.price.toLocaleString('vi-VN')} VNĐ</p>
                                        <p class="card-text">Tồn kho: ${book.stock}</p>
                                        <div class="btn-group">
                                            <button class="btn btn-info" onclick="showDetailPopup(${JSON.stringify(book).replace(/"/g, '&quot;')})">Xem chi tiết</button>
                                            <button class="btn btn-success" onclick="addToCart(${book.id}, '${book.title}', ${book.price})">Thêm vào giỏ</button>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        `;
                    });
                }

                // Cập nhật phân trang
                pagination.innerHTML = '';
                if (data.has_previous) {
                    pagination.innerHTML += `
                        <li class="page-item">
                            <a class="page-link" href="#" data-page="${data.previous_page}">Trước</a>
                        </li>
                    `;
                }
                pagination.innerHTML += `
                    <li class="page-item disabled">
                        <span class="page-link">Trang ${data.current_page} / ${data.total_pages}</span>
                    </li>
                `;
                if (data.has_next) {
                    pagination.innerHTML += `
                        <li class="page-item">
                            <a class="page-link" href="#" data-page="${data.next_page}">Sau</a>
                        </li>
                    `;
                }

                // Thêm sự kiện cho các nút phân trang
                document.querySelectorAll('.page-link').forEach(link => {
                    link.addEventListener('click', function(e) {
                        e.preventDefault();
                        currentPage = parseInt(this.getAttribute('data-page'));
                        fetchBooks(currentPage, currentQuery);
                    });
                });
            })
            .catch(error => {
                console.error('Error:', error);
                bookList.innerHTML = '<p>Đã có lỗi xảy ra. Vui lòng thử lại.</p>';
            });
    }

    // Sự kiện tìm kiếm
    searchInput.addEventListener('input', function() {
        currentQuery = this.value;
        currentPage = 1;  // Reset về trang 1 khi tìm kiếm
        fetchBooks(currentPage, currentQuery);
    });

    searchButton.addEventListener('click', function(e) {
        e.preventDefault();
        currentQuery = searchInput.value;
        currentPage = 1;
        fetchBooks(currentPage, currentQuery);
    });

    // Thêm sự kiện click cho các danh mục
document.querySelectorAll('.danh-muc-item').forEach(item => {
    item.addEventListener('click', function() {
        document.querySelectorAll('.danh-muc-item').forEach(i => i.classList.remove('active'));
        this.classList.add('active');

        const categoryName = this.querySelector('img').getAttribute('alt');
        const categoryId = getCategoryId(categoryName); // Chuyển tên thành id

        currentPage = 1;
        fetchBooks(currentPage, currentQuery, categoryId);
    });
});

// Hàm chuyển tên danh mục → id
function getCategoryId(categoryName) {
    const categoryMap = {
        'Văn học': 1,
        'Khoa học': 2,
        'Tâm lý': 3,
        'Tiểu thuyết': 4,
        'Lịch sử': 5,
        'Kỹ năng sống': 6,
        'Thiếu nhi': 7,
        'Công nghệ': 8,
        'Triết học': 9
    };
    return categoryMap[categoryName] || '';
}
if (allCategoryBtn) {
    allCategoryBtn.addEventListener('click', function () {
        // Xóa class active khỏi các mục danh mục
        document.querySelectorAll('.danh-muc-item').forEach(item => item.classList.remove('active'));

        // Làm trống tìm kiếm nếu muốn
        document.getElementById('search-input').value = '';
        currentQuery = '';
        currentPage = 1;

        // Gọi lại API không truyền category => load tất cả sách
        fetchBooks(currentPage, currentQuery, '');
    });
}
    // Lấy danh sách sách ban đầu
    fetchBooks(currentPage, currentQuery);
});
// Khởi tạo biến
const API_BASE_URL = 'http://localhost:8000';

// Hàm khởi tạo
document.addEventListener('DOMContentLoaded', function() {
    // Toggle Sidebar
    const sidebarCollapse = document.getElementById('sidebarCollapse');
    const sidebar = document.getElementById('sidebar');
    
    if (sidebarCollapse) {
        sidebarCollapse.addEventListener('click', function() {
            sidebar.classList.toggle('active');
        });
    }
    
    // Load dashboard data
    loadDashboardData();
});

// Hàm load dữ liệu dashboard
async function loadDashboardData() {
    try {
        // Load tổng số sách
        const booksResponse = await fetch(`${API_BASE_URL}/products/api/books/`);
        const booksData = await booksResponse.json();
        document.getElementById('totalBooks').textContent = booksData.count;
        
        // Load đơn hàng hôm nay
        const today = new Date().toISOString().split('T')[0];
        const ordersResponse = await fetch(`${API_BASE_URL}/orders/api/orders/?created_at__date=${today}`);
        const ordersData = await ordersResponse.json();
        document.getElementById('todayOrders').textContent = ordersData.count;
        
        // Load doanh thu hôm nay
        const salesResponse = await fetch(`${API_BASE_URL}/reports/api/sales/daily_sales/?days=1`);
        const salesData = await salesResponse.json();
        const todayRevenue = salesData[0]?.total_sales || 0;
        document.getElementById('todayRevenue').textContent = formatCurrency(todayRevenue);
        
        // Load sách sắp hết
        const lowStockResponse = await fetch(`${API_BASE_URL}/products/api/books/low_stock/?threshold=10`);
        const lowStockData = await lowStockResponse.json();
        document.getElementById('lowStock').textContent = lowStockData.length;
    } catch (error) {
        console.error('Lỗi khi tải dữ liệu dashboard:', error);
    }
}

// Hàm format tiền tệ
function formatCurrency(amount) {
    return new Intl.NumberFormat('vi-VN', {
        style: 'currency',
        currency: 'VND'
    }).format(amount);
}

// Hàm hiển thị thông báo
function showMessage(message, type = 'success') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    const container = document.querySelector('.container-fluid');
    container.insertBefore(alertDiv, container.firstChild);
    
    setTimeout(() => {
        alertDiv.remove();
    }, 3000);
} 
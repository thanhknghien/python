async function fetchAPI(endpoint, method = 'GET', body = null) {
    const token = localStorage.getItem('token');
    const headers = {
        'Content-Type': 'application/json',
    };
    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }
    const response = await fetch(`http://localhost:8000/api/books/${endpoint}`, {
        method,
        headers,
        body: body ? JSON.stringify(body) : null
    });
    const data = await response.json();  // Chuyển response thành JSON
    console.log(`Response from ${endpoint}:`, data);  // Log dữ liệu JSON
    if (!response.ok) throw new Error(`API request failed: ${response.status}`);
    return data;
}
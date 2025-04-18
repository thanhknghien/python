const testUser = {
    id : "1",
    username: "nguyenvana",
    password: "12345678",            
    role: "customer",
    full_name: "Nguyễn Văn A",
    address: "123 Đường ABC, Quận 1, TP.HCM",
    email: "nguyenvana@example.com",
    phone: "0901234567",
    status: "active"
  };

const test = localStorage.setItem('user', JSON.stringify(testUser))



const cart = localStorage.getItem('cart')||''
const user = localStorage.getItem('user')||''
let orders 
console.log(user)


fetch('/api/view_order/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ id: 1 })
})
  .then(res => res.text())  
  .then(text => {
      console.log('Response:', text);  
      try {
          const data = JSON.parse(text);  
          console.log('Hóa đơn của user:', data);
      } catch (err) {
          console.error('Lỗi parse JSON:', err);
      }
  })
  .catch(err => console.error('Lỗi:', err));



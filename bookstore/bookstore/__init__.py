import pymysql

# Kết nối đến cơ sở dữ liệu MySQL
connection = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    database='bookstore'
)

# Tạo con trỏ để thực thi câu lệnh SQL
cursor = connection.cursor()

# Thực thi câu lệnh SQL

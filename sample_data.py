import os
import django
from django.db import connection
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'boms.settings')
django.setup()

from bookstore.models import User, Category, Book, Order, OrderDetail, StockIn, StockOut

def populate_sample_data():
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='bookstore_category'")
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='bookstore_book'")
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='bookstore_user'")
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='bookstore_stokin'")
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='bookstore_stockout'")
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='bookstore_orderdetail'")
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='bookstore_order'")
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
        Category(name='Văn học'),
        Category(name='Khoa học'),
        Category(name='Tâm lý'),
        Category(name='Tiểu thuyết'),
        Category(name='Lịch sử'),
        Category(name='Kỹ năng sống'),
        Category(name='Thiếu nhi'),
        Category(name='Công nghệ'),
        Category(name='Triết học'),
    ]
    Category.objects.bulk_create(categories)
    print("Added Categories")

    # Refresh category list from DB để lấy ID mới
    categories = list(Category.objects.all())
    sample_books = [
    {
        "id":"1",
        "title": "Đắc Nhân Tâm",
        "author": "Dale Carnegie",
        "price": 120000,
        "stock": 15,
        "category": categories[2],  # Tâm lý
        "imagePath" : "book_images/1.jpg",
        "status": "available",
        "description": "Đắc nhân tâm là quyển sách nổi tiếng nhất, bán chạy nhất và có tầm ảnh hưởng nhất của mọi thời đại do Dale Carnegie viết. Đây là cuốn sách duy nhất về thể loại self-help liên tục đứng đầu danh mục sách bán chạy nhất (best-selling Books) do báo The New York Times bình chọn suốt 10 năm liền."
    },
    {
        "id":"2",
        "title": "Nhà Giả Kim",
        "author": "Paulo Coelho",
        "price": 89000,
        "stock": 20,
        "category": categories[3],  # Tiểu thuyết
        "imagePath" : "book_images/2.jpg",
        "status": "available",
        "description": "Tác phẩm kể về Santiago, một cậu bé chăn cừu đã dũng cảm dấn thân vào việc theo đuổi vận mệnh của mình. Một câu chuyện triết lý về việc dõi theo giấc mơ và lắng nghe tiếng nói con tim."
    },
    {
        "id":"3",
        "title": "Sapiens: Lược Sử Loài Người",
        "author": "Yuval Noah Harari",
        "price": 180000,
        "stock": 10,
        "category": categories[0],  # Khoa học
        "imagePath" : "book_images/3.jpg",
        "status": "available",
        "description": "Sapiens là một câu chuyện lịch sử đầy táo bạo và mới mẻ về cách con người đã tiến hóa từ những loài vượn tầm thường. Cuốn sách tóm tắt toàn bộ lịch sử loài người qua bốn cuộc cách mạng: nhận thức, nông nghiệp, văn minh và khoa học."
    },
    {
        "id":"4",
        "title": "Kinh Tế Học Hài Hước",
        "author": "Steven D. Levitt & Stephen J. Dubner",
        "price": 135000,
        "stock": 8,
        "category": categories[1],  # Kinh tế
        "imagePath" : "book_images/4.jpg",
        "status": "available",
        "description": "Cuốn sách ứng dụng những công cụ của kinh tế học để lý giải những hiện tượng xã hội phức tạp một cách dí dỏm. Từ việc phân tích tội phạm đến các chiến lược nuôi dạy con, cuốn sách đem đến một góc nhìn mới về thế giới."
    },
    {
        "id":"5",
        "title": "Chiến Tranh Tiền Tệ",
        "author": "Song Hongbing",
        "price": 150000,
        "stock": 5,
        "category": categories[1],  # Kinh tế
        "imagePath" : "book_images/5.jpg",
        "status": "available",
        "description": "Tác phẩm nghiên cứu về lịch sử và bản chất của tiền tệ, cũng như ảnh hưởng của nó đến các sự kiện lịch sử quan trọng. Cuốn sách đã gây ra nhiều tranh cãi về âm mưu của các nhà tài phiệt ngân hàng quốc tế."
    },
    {
        "id":"6",
        "title": "Việt Nam Sử Lược",
        "author": "Trần Trọng Kim",
        "price": 160000,
        "stock": 7,
        "category": categories[4],  # Lịch sử
        "imagePath" : "book_images/6.jpg",
        "status": "available",
        "description": "Cuốn sách viết về lịch sử Việt Nam từ thời kỳ dựng nước đến thời Pháp thuộc. Đây là công trình nghiên cứu lịch sử có giá trị cao, được viết bằng lối văn xuôi dễ đọc, dễ hiểu."
    },
    {
        "id":"7",
        "title": "Tâm Lý Học Đám Đông",
        "author": "Gustave Le Bon",
        "price": 95000,
        "stock": 0,
        "category": categories[2],  # Tâm lý
        "imagePath" : "book_images/7.jpg",
        "status": "unavailable",
        "description": "Nghiên cứu đầu tiên về tâm lý học đám đông và sự ảnh hưởng của nó đến xã hội. Cuốn sách phân tích những đặc điểm tâm lý của đám đông và cách thức mà các cá nhân thay đổi hành vi khi là một phần của tập thể."
    },
    {
        "id":"8",
        "title": "Hoàng Hôn Rực Rỡ",
        "author": "Khaled Hosseini",
        "price": 140000,
        "stock": 18,
        "category": categories[3],  # Tiểu thuyết
        "imagePath" : "book_images/8.jpg",
        "status": "available",
        "description": "Câu chuyện cảm động về tình bạn, sự phản bội và sự cứu chuộc, diễn ra trên nền Afghanistan đầy biến động. Một tác phẩm xuất sắc về tình người trong hoàn cảnh khó khăn."
    },
    {
        "id":"9",
        "title": "Vật Lý Vui",
        "author": "Walter Lewin",
        "price": 125000,
        "stock": 14,
        "category": categories[0],  # Khoa học
        "imagePath" : "book_images/9.jpg",
        "status": "available",
        "description": "Cuốn sách làm cho vật lý trở nên thú vị và dễ hiểu thông qua các thí nghiệm đơn giản và thú vị. Tác giả là giáo sư nổi tiếng tại MIT với phong cách giảng dạy đầy cuốn hút."
    },
    {
        "id":"10",
        "title": "Người Trong Muôn Nghề",
        "author": "Spiderum",
        "price": 145000,
        "stock": 22,
        "category": categories[5],  # Kỹ năng sống
        "imagePath" : "book_images/10.jpg",
        "status": "available",
        "description": "Tuyển tập những câu chuyện thật từ những người đang làm việc trong nhiều lĩnh vực khác nhau. Cuốn sách cung cấp góc nhìn thực tế về thế giới công việc và các ngành nghề tại Việt Nam hiện nay."
    },
    {
        "id":"11",
        "title": "Dế Mèn Phiêu Lưu Ký",
        "author": "Tô Hoài",
        "price": 75000,
        "stock": 30,
        "category": categories[6],  # Thiếu nhi
        "imagePath" : "book_images/11.jpg",
        "status": "available",
        "description": "Tác phẩm kinh điển của văn học thiếu nhi Việt Nam kể về cuộc phiêu lưu của chú Dế Mèn. Qua đó, truyền tải những bài học về lòng dũng cảm, tình bạn và trách nhiệm."
    },
    {
        "id":"12",
        "title": "Trí Tuệ Nhân Tạo",
        "author": "Kai-Fu Lee",
        "price": 195000,
        "stock": 8,
        "category": categories[7],  # Công nghệ
        "imagePath" : "book_images/12.jpg",
        "status": "available",
        "description": "Cuốn sách về AI và tương lai của loài người. Tác giả Kai-Fu Lee, một chuyên gia hàng đầu về AI, phân tích tác động của công nghệ này đến việc làm, xã hội và kinh tế toàn cầu."
    },
    {
        "id":"13",
        "title": "Bứt Phá Giới Hạn Bản Thân",
        "author": "Tony Robbins",
        "price": 168000,
        "stock": 16,
        "category": categories[5],  # Kỹ năng sống
        "imagePath" : "book_images/13.jpg",
        "status": "available",
        "description": "Cuốn sách hướng dẫn cách vượt qua những rào cản tâm lý và phát huy tiềm năng bản thân. Tony Robbins chia sẻ những chiến lược thực tế để đạt được thành công và hạnh phúc."
    },
    {
        "id":"14",
        "title": "Thế Giới Phẳng",
        "author": "Thomas L. Friedman",
        "price": 210000,
        "stock": 7,
        "category": categories[1],  # Kinh tế
        "imagePath" : "book_images/14.jpg",
        "status": "available",
        "description": "Phân tích về quá trình toàn cầu hóa và những thay đổi về kinh tế, xã hội trong thế kỷ 21. Cuốn sách giải thích làm thế nào công nghệ đã làm 'phẳng' thế giới và tạo ra sự cạnh tranh toàn cầu."
    },
    {
        "id":"15",
        "title": "Nghệ Thuật Tư Duy Rành Mạch",
        "author": "Rolf Dobelli",
        "price": 130000,
        "stock": 19,
        "category": categories[2],  # Tâm lý
        "imagePath" : "book_images/15.jpg",
        "status": "available",
        "description": "Tổng hợp 99 lỗi tư duy phổ biến và cách khắc phục chúng. Cuốn sách giúp người đọc nhận biết các thiên kiến nhận thức và đưa ra quyết định sáng suốt hơn."
    },
    {
        "id":"16",
        "title": "Lược Sử Thời Gian",
        "author": "Stephen Hawking",
        "price": 155000,
        "stock": 11,
        "category": categories[0],  # Khoa học
        "imagePath" : "book_images/16.jpg",
        "status": "available",
        "description": "Tác phẩm nổi tiếng giải thích các khái niệm phức tạp của vật lý hiện đại như lỗ đen, vũ trụ giãn nở và thuyết tương đối bằng ngôn ngữ dễ hiểu cho độc giả phổ thông."
    },
    {
        "id":"17",
        "title": "Tôi Tài Giỏi, Bạn Cũng Thế",
        "author": "Adam Khoo",
        "price": 110000,
        "stock": 25,
        "category": categories[5],  # Kỹ năng sống
        "imagePath" : "book_images/17.jpg",
        "status": "available",
        "description": "Phương pháp học tập hiệu quả và phát triển tư duy tích cực. Cuốn sách chia sẻ những kỹ thuật học tập nhanh, ghi nhớ tốt và tư duy sáng tạo."
    },
    {
        "id":"18",
        "title": "Triết Học Nghệ Thuật Sống",
        "author": "Luc Ferry",
        "price": 148000,
        "stock": 6,
        "category": categories[8],  # Triết học
        "imagePath" : "book_images/18.jpg",
        "status": "available",
        "description": "Cuốn sách giới thiệu về các trường phái triết học lớn và cách áp dụng vào"
    }
]

    # Tạo danh sách book objects
    book_objects = []
    for book_data in sample_books:
        if not Book.objects.filter(title=book_data["title"]).exists():
            book = Book(
                title=book_data["title"],
                author=book_data["author"],
                price=book_data["price"],
                stock=book_data["stock"],
                category=book_data["category"],
                imagePath=book_data["imagePath"],
                status=book_data["status"],
                description=book_data["description"]
            )
            book_objects.append(book)

    if book_objects:
        Book.objects.bulk_create(book_objects)
        print(f'Đã tạo thành công {len(book_objects)} sách mẫu')
    else:
        print('Không có sách mới để tạo')

    

if __name__ == '__main__':
    populate_sample_data()
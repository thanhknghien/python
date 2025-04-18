INSERT INTO category (name) VALUES 
('Văn học'),
('Khoa học'),
('Tâm lý'),
('Tiểu thuyết'),
('Lịch sử'),
('Kỹ năng sống'),
('Thiếu nhi'),
('Công nghệ'),
('Triết học');


INSERT INTO bookstore_book (id, title, author, price, stock, category_id, imagePath, status, description) VALUES
(1, 'Đắc Nhân Tâm', 'Dale Carnegie', 120000, 15, 3, 'book_images/1.jpg', 'available', 'Đắc nhân tâm là quyển sách nổi tiếng nhất...'),
(2, 'Nhà Giả Kim', 'Paulo Coelho', 89000, 20, 4, 'book_images/2.jpg', 'available', 'Tác phẩm kể về Santiago...'),
(3, 'Sapiens: Lược Sử Loài Người', 'Yuval Noah Harari', 180000, 10, 2, 'book_images/3.jpg', 'available', 'Sapiens là một câu chuyện lịch sử...'),
(4, 'Kinh Tế Học Hài Hước', 'Steven D. Levitt & Stephen J. Dubner', 135000, 8, 2, 'book_images/4.jpg', 'available', 'Cuốn sách ứng dụng những công cụ của kinh tế học...'),
(5, 'Chiến Tranh Tiền Tệ', 'Song Hongbing', 150000, 5, 2, 'book_images/5.jpg', 'available', 'Tác phẩm nghiên cứu về lịch sử và bản chất của tiền tệ...'),
(6, 'Việt Nam Sử Lược', 'Trần Trọng Kim', 160000, 7, 5, 'book_images/6.jpg', 'available', 'Cuốn sách viết về lịch sử Việt Nam...'),
(7, 'Tâm Lý Học Đám Đông', 'Gustave Le Bon', 95000, 0, 3, 'book_images/7.jpg', 'unavailable', 'Nghiên cứu đầu tiên về tâm lý học đám đông...'),
(8, 'Hoàng Hôn Rực Rỡ', 'Khaled Hosseini', 140000, 18, 4, 'book_images/8.jpg', 'available', 'Câu chuyện cảm động về tình bạn...'),
(9, 'Vật Lý Vui', 'Walter Lewin', 125000, 14, 2, 'book_images/9.jpg', 'available', 'Cuốn sách làm cho vật lý trở nên thú vị...'),
(10, 'Người Trong Muôn Nghề', 'Spiderum', 145000, 22, 6, 'book_images/10.jpg', 'available', 'Tuyển tập những câu chuyện thật từ những người đang làm việc...'),
(11, 'Dế Mèn Phiêu Lưu Ký', 'Tô Hoài', 75000, 30, 7, 'book_images/11.jpg', 'available', 'Tác phẩm kinh điển của văn học thiếu nhi Việt Nam...'),
(12, 'Trí Tuệ Nhân Tạo', 'Kai-Fu Lee', 195000, 8, 8, 'book_images/12.jpg', 'available', 'Cuốn sách về AI và tương lai của loài người...'),
(13, 'Bứt Phá Giới Hạn Bản Thân', 'Tony Robbins', 168000, 16, 6, 'book_images/13.jpg', 'available', 'Cuốn sách hướng dẫn cách vượt qua những rào cản tâm lý...'),
(14, 'Thế Giới Phẳng', 'Thomas L. Friedman', 210000, 7, 2, 'book_images/14.jpg', 'available', 'Phân tích về quá trình toàn cầu hóa...'),
(15, 'Nghệ Thuật Tư Duy Rành Mạch', 'Rolf Dobelli', 130000, 19, 3, 'book_images/15.jpg', 'available', 'Tổng hợp 99 lỗi tư duy phổ biến...'),
(16, 'Lược Sử Thời Gian', 'Stephen Hawking', 155000, 11, 2, 'book_images/16.jpg', 'available', 'Tác phẩm nổi tiếng giải thích các khái niệm phức tạp...'),
(17, 'Tôi Tài Giỏi, Bạn Cũng Thế', 'Adam Khoo', 110000, 25, 6, 'book_images/17.jpg', 'available', 'Phương pháp học tập hiệu quả và phát triển tư duy...'),
(18, 'Triết Học Nghệ Thuật Sống', 'Luc Ferry', 148000, 6, 9, 'book_images/18.jpg', 'available', 'Cuốn sách giới thiệu về các trường phái triết học lớn...');

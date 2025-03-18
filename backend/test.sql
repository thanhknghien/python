
CREATE DATABASE IF NOT EXISTS `bookstore_web` 
USE `bookstore_web`;

CREATE TABLE IF NOT EXISTS `accounts_account` (
  `AccountID` int(11) NOT NULL AUTO_INCREMENT,
  `Username` varchar(30) NOT NULL,
  `Password` varchar(255) NOT NULL,
  `FullName` varchar(20) NOT NULL,
  `Email` varchar(50) NOT NULL,
  `Phone` varchar(15) NOT NULL,
  `Address` varchar(200) NOT NULL,
  `EmployeeID_id` int(11) DEFAULT NULL,
  `RoleID_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`AccountID`),
  UNIQUE KEY `Username` (`Username`),
  KEY `accounts_account_EmployeeID_id_85a76ba8_fk_accounts_` (`EmployeeID_id`),
  KEY `accounts_account_RoleID_id_629247f8_fk_accounts_role_RoleID` (`RoleID_id`),
  CONSTRAINT `accounts_account_EmployeeID_id_85a76ba8_fk_accounts_` FOREIGN KEY (`EmployeeID_id`) REFERENCES `accounts_employee` (`EmployeeID`),
  CONSTRAINT `accounts_account_RoleID_id_629247f8_fk_accounts_role_RoleID` FOREIGN KEY (`RoleID_id`) REFERENCES `accounts_role` (`RoleID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_uca1400_ai_ci;

CREATE TABLE IF NOT EXISTS `accounts_employee` (
  `EmployeeID` int(11) NOT NULL AUTO_INCREMENT,
  `Status` varchar(20) NOT NULL,
  PRIMARY KEY (`EmployeeID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_uca1400_ai_ci;

CREATE TABLE IF NOT EXISTS `accounts_permission` (
  `PermissionID` int(11) NOT NULL AUTO_INCREMENT,
  `PermissionName` varchar(50) NOT NULL,
  PRIMARY KEY (`PermissionID`),
  UNIQUE KEY `PermissionName` (`PermissionName`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_uca1400_ai_ci;

CREATE TABLE IF NOT EXISTS `accounts_role` (
  `RoleID` int(11) NOT NULL AUTO_INCREMENT,
  `RoleName` varchar(30) NOT NULL,
  PRIMARY KEY (`RoleID`),
  UNIQUE KEY `RoleName` (`RoleName`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_uca1400_ai_ci;

CREATE TABLE IF NOT EXISTS `accounts_rolepermission` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `PermissionID_id` int(11) NOT NULL,
  `RoleID_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_role_permission` (`RoleID_id`,`PermissionID_id`),
  KEY `accounts_rolepermiss_PermissionID_id_475d7dcc_fk_accounts_` (`PermissionID_id`),
  CONSTRAINT `accounts_rolepermiss_PermissionID_id_475d7dcc_fk_accounts_` FOREIGN KEY (`PermissionID_id`) REFERENCES `accounts_permission` (`PermissionID`),
  CONSTRAINT `accounts_rolepermiss_RoleID_id_4aee3116_fk_accounts_` FOREIGN KEY (`RoleID_id`) REFERENCES `accounts_role` (`RoleID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_uca1400_ai_ci;

CREATE TABLE IF NOT EXISTS `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_uca1400_ai_ci;

CREATE TABLE IF NOT EXISTS `auth_group_permissions` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_uca1400_ai_ci;

CREATE TABLE IF NOT EXISTS `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=77 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_uca1400_ai_ci;

CREATE TABLE IF NOT EXISTS `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_uca1400_ai_ci;

CREATE TABLE IF NOT EXISTS `auth_user_groups` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_uca1400_ai_ci;

CREATE TABLE IF NOT EXISTS `auth_user_user_permissions` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_uca1400_ai_ci;

CREATE TABLE IF NOT EXISTS `books_book` (
  `BookID` int(11) NOT NULL AUTO_INCREMENT,
  `Title` varchar(100) NOT NULL,
  `Author` varchar(50) DEFAULT NULL,
  `Genre` varchar(30) DEFAULT NULL,
  `Price` decimal(10,2) NOT NULL,
  `StockQuantity` int(11) NOT NULL,
  `ImagePath` varchar(255) DEFAULT NULL,
  `CategoryID_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`BookID`),
  KEY `books_book_CategoryID_id_b655d05d_fk_books_category_CategoryID` (`CategoryID_id`),
  CONSTRAINT `books_book_CategoryID_id_b655d05d_fk_books_category_CategoryID` FOREIGN KEY (`CategoryID_id`) REFERENCES `books_category` (`CategoryID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_uca1400_ai_ci;

CREATE TABLE IF NOT EXISTS `books_category` (
  `CategoryID` int(11) NOT NULL AUTO_INCREMENT,
  `Name` varchar(50) NOT NULL,
  PRIMARY KEY (`CategoryID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_uca1400_ai_ci;

CREATE TABLE IF NOT EXISTS `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_uca1400_ai_ci;

CREATE TABLE IF NOT EXISTS `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_uca1400_ai_ci;

CREATE TABLE IF NOT EXISTS `django_migrations` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_uca1400_ai_ci;

CREATE TABLE IF NOT EXISTS `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_uca1400_ai_ci;

CREATE TABLE IF NOT EXISTS `imports_importslip` (
  `SlipID` int(11) NOT NULL AUTO_INCREMENT,
  `ImportDate` datetime(6) NOT NULL,
  `TotalAmount` decimal(10,2) NOT NULL,
  `EmployeeID_id` int(11) DEFAULT NULL,
  `SupplierID_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`SlipID`),
  KEY `imports_importslip_EmployeeID_id_4cb1f262_fk_accounts_` (`EmployeeID_id`),
  KEY `imports_importslip_SupplierID_id_00ed7aba_fk_suppliers` (`SupplierID_id`),
  CONSTRAINT `imports_importslip_EmployeeID_id_4cb1f262_fk_accounts_` FOREIGN KEY (`EmployeeID_id`) REFERENCES `accounts_employee` (`EmployeeID`),
  CONSTRAINT `imports_importslip_SupplierID_id_00ed7aba_fk_suppliers` FOREIGN KEY (`SupplierID_id`) REFERENCES `suppliers_supplier` (`SupplierID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_uca1400_ai_ci;

CREATE TABLE IF NOT EXISTS `imports_importslipdetail` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `Quantity` int(11) NOT NULL,
  `UnitPrice` decimal(10,2) NOT NULL,
  `BookID_id` int(11) NOT NULL,
  `SlipID_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_slip_book` (`SlipID_id`,`BookID_id`),
  KEY `imports_importslipdetail_BookID_id_42328525_fk_books_book_BookID` (`BookID_id`),
  CONSTRAINT `imports_importslipde_SlipID_id_8c26233c_fk_imports_i` FOREIGN KEY (`SlipID_id`) REFERENCES `imports_importslip` (`SlipID`),
  CONSTRAINT `imports_importslipdetail_BookID_id_42328525_fk_books_book_BookID` FOREIGN KEY (`BookID_id`) REFERENCES `books_book` (`BookID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_uca1400_ai_ci;

CREATE TABLE IF NOT EXISTS `orders_orderdetail` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `Quantity` int(11) NOT NULL,
  `UnitPrice` decimal(10,2) NOT NULL,
  `BookID_id` int(11) NOT NULL,
  `OrderID_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_order_book` (`OrderID_id`,`BookID_id`),
  KEY `orders_orderdetail_BookID_id_54d45cd3_fk_books_book_BookID` (`BookID_id`),
  CONSTRAINT `orders_orderdetail_BookID_id_54d45cd3_fk_books_book_BookID` FOREIGN KEY (`BookID_id`) REFERENCES `books_book` (`BookID`),
  CONSTRAINT `orders_orderdetail_OrderID_id_369ab530_fk_orders_orders_OrderID` FOREIGN KEY (`OrderID_id`) REFERENCES `orders_orders` (`OrderID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_uca1400_ai_ci;

CREATE TABLE IF NOT EXISTS `orders_orders` (
  `OrderID` int(11) NOT NULL AUTO_INCREMENT,
  `OrderDate` datetime(6) NOT NULL,
  `TotalAmount` decimal(10,2) NOT NULL,
  `Status` varchar(20) NOT NULL,
  `CustomerID_id` int(11) NOT NULL,
  `EmployeeID_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`OrderID`),
  KEY `orders_orders_CustomerID_id_92eb8294_fk_accounts_` (`CustomerID_id`),
  KEY `orders_orders_EmployeeID_id_a82d75cf_fk_accounts_` (`EmployeeID_id`),
  CONSTRAINT `orders_orders_CustomerID_id_92eb8294_fk_accounts_` FOREIGN KEY (`CustomerID_id`) REFERENCES `accounts_account` (`AccountID`),
  CONSTRAINT `orders_orders_EmployeeID_id_a82d75cf_fk_accounts_` FOREIGN KEY (`EmployeeID_id`) REFERENCES `accounts_employee` (`EmployeeID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_uca1400_ai_ci;

CREATE TABLE IF NOT EXISTS `promotions_promotion` (
  `PromotionID` int(11) NOT NULL AUTO_INCREMENT,
  `Name` varchar(50) NOT NULL,
  `DiscountPercent` decimal(5,2) NOT NULL,
  `StartDate` date NOT NULL,
  `EndDate` date NOT NULL,
  `CategoryID_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`PromotionID`),
  KEY `promotions_promotion_CategoryID_id_cf816c05_fk_books_cat` (`CategoryID_id`),
  CONSTRAINT `promotions_promotion_CategoryID_id_cf816c05_fk_books_cat` FOREIGN KEY (`CategoryID_id`) REFERENCES `books_category` (`CategoryID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_uca1400_ai_ci;

CREATE TABLE IF NOT EXISTS `suppliers_supplier` (
  `SupplierID` int(11) NOT NULL AUTO_INCREMENT,
  `SupplierName` varchar(50) NOT NULL,
  `SupplierNumber` varchar(15) NOT NULL,
  `SupplierAddress` varchar(200) NOT NULL,
  `Status` varchar(20) NOT NULL,
  PRIMARY KEY (`SupplierID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3 COLLATE=utf8mb3_uca1400_ai_ci;

-- Thêm dữ liệu mẫu cho bảng accounts_employee
INSERT INTO accounts_employee (Status) VALUES 
('Active'),
('Inactive'),
('On Leave');

-- Thêm dữ liệu mẫu cho bảng accounts_role
INSERT INTO accounts_role (RoleName) VALUES 
('Admin'),
('Sales Staff'),
('Warehouse Staff'),
('Customer');

-- Thêm dữ liệu mẫu cho bảng accounts_account
INSERT INTO accounts_account (Username, Password, FullName, Email, Phone, Address, EmployeeID_id, RoleID_id) VALUES
('admin', 'admin123', 'John Doe', 'admin@example.com', '123456789', '123 Admin St', 1, 1),
('staff1', 'staff123', 'Alice Smith', 'alice@example.com', '987654321', '456 Staff St', 2, 2),
('customer1', 'cust123', 'Bob Johnson', 'bob@example.com', '555666777', '789 Customer St', NULL, 4);

-- Thêm dữ liệu mẫu cho bảng accounts_permission
INSERT INTO accounts_permission (PermissionName) VALUES 
('View Orders'),
('Manage Orders'),
('Manage Inventory'),
('Manage Accounts');

-- Thêm dữ liệu mẫu cho bảng accounts_rolepermission
INSERT INTO accounts_rolepermission (RoleID_id, PermissionID_id) VALUES 
(1, 1), -- Admin có thể xem đơn hàng
(1, 2), -- Admin có thể quản lý đơn hàng
(1, 3), -- Admin có thể quản lý kho
(1, 4), -- Admin có thể quản lý tài khoản
(2, 1), -- Nhân viên bán hàng có thể xem đơn hàng
(2, 2), -- Nhân viên bán hàng có thể quản lý đơn hàng
(3, 3), -- Nhân viên kho có thể quản lý kho
(4, 1); -- Khách hàng có thể xem đơn hàng của mình

-- Thêm dữ liệu mẫu cho bảng books_category
INSERT INTO books_category (Name) VALUES 
('Fiction'),
('Science'),
('History'),
('Technology');

-- Thêm dữ liệu mẫu cho bảng books_book
INSERT INTO books_book (Title, Author, Genre, Price, StockQuantity, ImagePath, CategoryID_id) VALUES 
('The Great Gatsby', 'F. Scott Fitzgerald', 'Fiction', 10.99, 50, NULL, 1),
('A Brief History of Time', 'Stephen Hawking', 'Science', 15.99, 30, NULL, 2),
('Sapiens', 'Yuval Noah Harari', 'History', 12.99, 40, NULL, 3),
('Clean Code', 'Robert C. Martin', 'Technology', 25.99, 20, NULL, 4);

-- Thêm dữ liệu mẫu cho bảng orders_orders
INSERT INTO orders_orders (OrderDate, TotalAmount, Status, CustomerID_id, EmployeeID_id) VALUES 
(NOW(), 21.98, 'Processing', 3, 2),
(NOW(), 15.99, 'Shipped', 3, 2);

-- Thêm dữ liệu mẫu cho bảng orders_orderdetail
INSERT INTO orders_orderdetail (Quantity, UnitPrice, BookID_id, OrderID_id) VALUES 
(1, 10.99, 1, 1),
(1, 10.99, 2, 1),
(1, 15.99, 3, 2);

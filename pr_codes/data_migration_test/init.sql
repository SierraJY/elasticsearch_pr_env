-- 기존 articles 테이블 삭제 (필요 없으면 생략 가능)
DROP TABLE IF EXISTS articles;

-- eCommerce Orders 테이블 생성
CREATE TABLE IF NOT EXISTS ecommerce_orders (
  order_id SERIAL PRIMARY KEY,
  customer_full_name VARCHAR(255) NOT NULL,
  order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  total_quantity INTEGER,
  total_unique_products INTEGER,
  product_name TEXT
);

-- 샘플 데이터 삽입 (여러 개 추가 가능)
INSERT INTO ecommerce_orders (customer_full_name, order_date, total_quantity, total_unique_products, product_name) VALUES
('Eddie Underwood', '2025-03-10 09:28:48', 2, 2, 'Basic T-shirt - dark blue/white, Sweatshirt - grey multicolor'),
('Sarah Johnson', '2025-03-12 14:15:20', 1, 1, 'Running Shoes - Black'),
('Michael Lee', '2025-03-15 18:45:35', 3, 2, 'Wireless Earbuds, Smartwatch'),
('Olivia Brown', '2025-03-18 10:30:55', 5, 4, 'Yoga Mat, Resistance Bands, Kettlebell, Dumbbells'),
('David Smith', '2025-03-20 12:10:40', 1, 1, 'Laptop - 16GB RAM, 512GB SSD');

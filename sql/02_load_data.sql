-- Load RetailPulse CSV files into MySQL.
-- Run this from the repo root:
-- mysql --local-infile=1 -u root -p retailpulse_analytics < sql/02_load_data.sql

USE retailpulse_analytics;

SET FOREIGN_KEY_CHECKS = 0;

LOAD DATA LOCAL INFILE 'data/customers.csv'
INTO TABLE customers
CHARACTER SET utf8mb4
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS
(customer_id, first_name, last_name, email, acquisition_channel, customer_segment, city, state, signup_date, status);

LOAD DATA LOCAL INFILE 'data/addresses.csv'
INTO TABLE addresses
CHARACTER SET utf8mb4
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS
(address_id, customer_id, address_type, street_address, city, state, postal_code, country, is_default);

LOAD DATA LOCAL INFILE 'data/categories.csv'
INTO TABLE categories
CHARACTER SET utf8mb4
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS
(category_id, category_name, description);

LOAD DATA LOCAL INFILE 'data/suppliers.csv'
INTO TABLE suppliers
CHARACTER SET utf8mb4
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS
(supplier_id, supplier_name, contact_email, city, state, country);

LOAD DATA LOCAL INFILE 'data/products.csv'
INTO TABLE products
CHARACTER SET utf8mb4
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS
(product_id, product_name, category_id, supplier_id, brand, unit_cost, unit_price, status, created_date);

LOAD DATA LOCAL INFILE 'data/warehouses.csv'
INTO TABLE warehouses
CHARACTER SET utf8mb4
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS
(warehouse_id, warehouse_name, city, state, capacity_units);

LOAD DATA LOCAL INFILE 'data/inventory.csv'
INTO TABLE inventory
CHARACTER SET utf8mb4
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS
(product_id, warehouse_id, quantity_on_hand, reorder_level, last_stock_check_date);

LOAD DATA LOCAL INFILE 'data/employees.csv'
INTO TABLE employees
CHARACTER SET utf8mb4
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS
(employee_id, first_name, last_name, department, job_title, @warehouse_id, hire_date, status)
SET warehouse_id = NULLIF(@warehouse_id, '');

LOAD DATA LOCAL INFILE 'data/orders.csv'
INTO TABLE orders
CHARACTER SET utf8mb4
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS
(order_id, customer_id, order_datetime, order_status, sales_channel, subtotal, discount_amount, tax_amount, shipping_fee, total_amount, @sales_rep_id)
SET sales_rep_id = NULLIF(@sales_rep_id, '');

LOAD DATA LOCAL INFILE 'data/order_items.csv'
INTO TABLE order_items
CHARACTER SET utf8mb4
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS
(order_item_id, order_id, product_id, quantity, unit_price, discount_amount, line_total);

LOAD DATA LOCAL INFILE 'data/payments.csv'
INTO TABLE payments
CHARACTER SET utf8mb4
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS
(payment_id, order_id, payment_method, payment_status, amount, payment_datetime);

LOAD DATA LOCAL INFILE 'data/shipments.csv'
INTO TABLE shipments
CHARACTER SET utf8mb4
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS
(shipment_id, order_id, warehouse_id, shipping_method, carrier, shipped_datetime, @delivered_datetime, shipment_status)
SET delivered_datetime = NULLIF(@delivered_datetime, '');

LOAD DATA LOCAL INFILE 'data/reviews.csv'
INTO TABLE reviews
CHARACTER SET utf8mb4
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS
(review_id, customer_id, product_id, order_id, rating, review_text, review_date);

LOAD DATA LOCAL INFILE 'data/support_tickets.csv'
INTO TABLE support_tickets
CHARACTER SET utf8mb4
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS
(ticket_id, customer_id, order_id, topic, ticket_status, priority, opened_datetime, @closed_datetime, assigned_employee_id)
SET closed_datetime = NULLIF(@closed_datetime, '');

LOAD DATA LOCAL INFILE 'data/returns.csv'
INTO TABLE returns
CHARACTER SET utf8mb4
FIELDS TERMINATED BY ',' ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS
(return_id, order_id, customer_id, return_reason, return_status, refund_amount, return_date);

SET FOREIGN_KEY_CHECKS = 1;

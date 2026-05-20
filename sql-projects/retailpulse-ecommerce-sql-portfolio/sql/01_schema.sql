-- RetailPulse Ecommerce SQL Portfolio
-- MySQL 8+ schema: normalized tables, keys, checks, and helpful indexes.

DROP DATABASE IF EXISTS retailpulse_analytics;
CREATE DATABASE retailpulse_analytics
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_0900_ai_ci;

USE retailpulse_analytics;

SET FOREIGN_KEY_CHECKS = 0;

CREATE TABLE customers (
  customer_id INT NOT NULL,
  first_name VARCHAR(50) NOT NULL,
  last_name VARCHAR(50) NOT NULL,
  email VARCHAR(120) NOT NULL,
  acquisition_channel VARCHAR(40) NOT NULL,
  customer_segment VARCHAR(30) NOT NULL,
  city VARCHAR(60) NOT NULL,
  state VARCHAR(30) NOT NULL,
  signup_date DATE NOT NULL,
  status VARCHAR(20) NOT NULL,
  PRIMARY KEY (customer_id),
  UNIQUE KEY uq_customers_email (email)
) ENGINE = InnoDB;

CREATE TABLE addresses (
  address_id INT NOT NULL,
  customer_id INT NOT NULL,
  address_type VARCHAR(20) NOT NULL,
  street_address VARCHAR(120) NOT NULL,
  city VARCHAR(60) NOT NULL,
  state VARCHAR(30) NOT NULL,
  postal_code VARCHAR(15) NOT NULL,
  country VARCHAR(40) NOT NULL,
  is_default TINYINT NOT NULL,
  PRIMARY KEY (address_id),
  CONSTRAINT fk_addresses_customer
    FOREIGN KEY (customer_id) REFERENCES customers (customer_id),
  CONSTRAINT chk_addresses_default_flag
    CHECK (is_default IN (0, 1))
) ENGINE = InnoDB;

CREATE TABLE categories (
  category_id INT NOT NULL,
  category_name VARCHAR(80) NOT NULL,
  description VARCHAR(255) NOT NULL,
  PRIMARY KEY (category_id),
  UNIQUE KEY uq_categories_name (category_name)
) ENGINE = InnoDB;

CREATE TABLE suppliers (
  supplier_id INT NOT NULL,
  supplier_name VARCHAR(120) NOT NULL,
  contact_email VARCHAR(120) NOT NULL,
  city VARCHAR(60) NOT NULL,
  state VARCHAR(30) NOT NULL,
  country VARCHAR(40) NOT NULL,
  PRIMARY KEY (supplier_id),
  UNIQUE KEY uq_suppliers_email (contact_email)
) ENGINE = InnoDB;

CREATE TABLE products (
  product_id INT NOT NULL,
  product_name VARCHAR(160) NOT NULL,
  category_id INT NOT NULL,
  supplier_id INT NOT NULL,
  brand VARCHAR(60) NOT NULL,
  unit_cost DECIMAL(10, 2) NOT NULL,
  unit_price DECIMAL(10, 2) NOT NULL,
  status VARCHAR(20) NOT NULL,
  created_date DATE NOT NULL,
  PRIMARY KEY (product_id),
  CONSTRAINT fk_products_category
    FOREIGN KEY (category_id) REFERENCES categories (category_id),
  CONSTRAINT fk_products_supplier
    FOREIGN KEY (supplier_id) REFERENCES suppliers (supplier_id),
  CONSTRAINT chk_products_cost_price
    CHECK (unit_cost >= 0 AND unit_price >= 0)
) ENGINE = InnoDB;

CREATE TABLE warehouses (
  warehouse_id INT NOT NULL,
  warehouse_name VARCHAR(100) NOT NULL,
  city VARCHAR(60) NOT NULL,
  state VARCHAR(30) NOT NULL,
  capacity_units INT NOT NULL,
  PRIMARY KEY (warehouse_id),
  CONSTRAINT chk_warehouses_capacity
    CHECK (capacity_units >= 0)
) ENGINE = InnoDB;

CREATE TABLE inventory (
  product_id INT NOT NULL,
  warehouse_id INT NOT NULL,
  quantity_on_hand INT NOT NULL,
  reorder_level INT NOT NULL,
  last_stock_check_date DATE NOT NULL,
  PRIMARY KEY (product_id, warehouse_id),
  CONSTRAINT fk_inventory_product
    FOREIGN KEY (product_id) REFERENCES products (product_id),
  CONSTRAINT fk_inventory_warehouse
    FOREIGN KEY (warehouse_id) REFERENCES warehouses (warehouse_id),
  CONSTRAINT chk_inventory_quantity
    CHECK (quantity_on_hand >= 0 AND reorder_level >= 0)
) ENGINE = InnoDB;

CREATE TABLE employees (
  employee_id INT NOT NULL,
  first_name VARCHAR(50) NOT NULL,
  last_name VARCHAR(50) NOT NULL,
  department VARCHAR(50) NOT NULL,
  job_title VARCHAR(80) NOT NULL,
  warehouse_id INT NULL,
  hire_date DATE NOT NULL,
  status VARCHAR(20) NOT NULL,
  PRIMARY KEY (employee_id),
  CONSTRAINT fk_employees_warehouse
    FOREIGN KEY (warehouse_id) REFERENCES warehouses (warehouse_id)
) ENGINE = InnoDB;

CREATE TABLE orders (
  order_id INT NOT NULL,
  customer_id INT NOT NULL,
  order_datetime DATETIME NOT NULL,
  order_status VARCHAR(30) NOT NULL,
  sales_channel VARCHAR(40) NOT NULL,
  subtotal DECIMAL(12, 2) NOT NULL,
  discount_amount DECIMAL(12, 2) NOT NULL,
  tax_amount DECIMAL(12, 2) NOT NULL,
  shipping_fee DECIMAL(12, 2) NOT NULL,
  total_amount DECIMAL(12, 2) NOT NULL,
  sales_rep_id INT NULL,
  PRIMARY KEY (order_id),
  CONSTRAINT fk_orders_customer
    FOREIGN KEY (customer_id) REFERENCES customers (customer_id),
  CONSTRAINT fk_orders_sales_rep
    FOREIGN KEY (sales_rep_id) REFERENCES employees (employee_id),
  CONSTRAINT chk_orders_amounts
    CHECK (
      subtotal >= 0
      AND discount_amount >= 0
      AND tax_amount >= 0
      AND shipping_fee >= 0
      AND total_amount >= 0
    )
) ENGINE = InnoDB;

CREATE TABLE order_items (
  order_item_id INT NOT NULL,
  order_id INT NOT NULL,
  product_id INT NOT NULL,
  quantity INT NOT NULL,
  unit_price DECIMAL(10, 2) NOT NULL,
  discount_amount DECIMAL(10, 2) NOT NULL,
  line_total DECIMAL(12, 2) NOT NULL,
  PRIMARY KEY (order_item_id),
  CONSTRAINT fk_order_items_order
    FOREIGN KEY (order_id) REFERENCES orders (order_id),
  CONSTRAINT fk_order_items_product
    FOREIGN KEY (product_id) REFERENCES products (product_id),
  CONSTRAINT chk_order_items_amounts
    CHECK (
      quantity > 0
      AND unit_price >= 0
      AND discount_amount >= 0
      AND line_total >= 0
    )
) ENGINE = InnoDB;

CREATE TABLE payments (
  payment_id INT NOT NULL,
  order_id INT NOT NULL,
  payment_method VARCHAR(40) NOT NULL,
  payment_status VARCHAR(40) NOT NULL,
  amount DECIMAL(12, 2) NOT NULL,
  payment_datetime DATETIME NOT NULL,
  PRIMARY KEY (payment_id),
  CONSTRAINT fk_payments_order
    FOREIGN KEY (order_id) REFERENCES orders (order_id),
  CONSTRAINT chk_payments_amount
    CHECK (amount >= 0)
) ENGINE = InnoDB;

CREATE TABLE shipments (
  shipment_id INT NOT NULL,
  order_id INT NOT NULL,
  warehouse_id INT NOT NULL,
  shipping_method VARCHAR(40) NOT NULL,
  carrier VARCHAR(40) NOT NULL,
  shipped_datetime DATETIME NOT NULL,
  delivered_datetime DATETIME NULL,
  shipment_status VARCHAR(40) NOT NULL,
  PRIMARY KEY (shipment_id),
  CONSTRAINT fk_shipments_order
    FOREIGN KEY (order_id) REFERENCES orders (order_id),
  CONSTRAINT fk_shipments_warehouse
    FOREIGN KEY (warehouse_id) REFERENCES warehouses (warehouse_id)
) ENGINE = InnoDB;

CREATE TABLE reviews (
  review_id INT NOT NULL,
  customer_id INT NOT NULL,
  product_id INT NOT NULL,
  order_id INT NOT NULL,
  rating INT NOT NULL,
  review_text VARCHAR(255) NOT NULL,
  review_date DATE NOT NULL,
  PRIMARY KEY (review_id),
  CONSTRAINT fk_reviews_customer
    FOREIGN KEY (customer_id) REFERENCES customers (customer_id),
  CONSTRAINT fk_reviews_product
    FOREIGN KEY (product_id) REFERENCES products (product_id),
  CONSTRAINT fk_reviews_order
    FOREIGN KEY (order_id) REFERENCES orders (order_id),
  CONSTRAINT chk_reviews_rating
    CHECK (rating BETWEEN 1 AND 5)
) ENGINE = InnoDB;

CREATE TABLE support_tickets (
  ticket_id INT NOT NULL,
  customer_id INT NOT NULL,
  order_id INT NOT NULL,
  topic VARCHAR(80) NOT NULL,
  ticket_status VARCHAR(40) NOT NULL,
  priority VARCHAR(20) NOT NULL,
  opened_datetime DATETIME NOT NULL,
  closed_datetime DATETIME NULL,
  assigned_employee_id INT NOT NULL,
  PRIMARY KEY (ticket_id),
  CONSTRAINT fk_support_tickets_customer
    FOREIGN KEY (customer_id) REFERENCES customers (customer_id),
  CONSTRAINT fk_support_tickets_order
    FOREIGN KEY (order_id) REFERENCES orders (order_id),
  CONSTRAINT fk_support_tickets_employee
    FOREIGN KEY (assigned_employee_id) REFERENCES employees (employee_id)
) ENGINE = InnoDB;

CREATE TABLE returns (
  return_id INT NOT NULL,
  order_id INT NOT NULL,
  customer_id INT NOT NULL,
  return_reason VARCHAR(80) NOT NULL,
  return_status VARCHAR(40) NOT NULL,
  refund_amount DECIMAL(12, 2) NOT NULL,
  return_date DATE NOT NULL,
  PRIMARY KEY (return_id),
  CONSTRAINT fk_returns_order
    FOREIGN KEY (order_id) REFERENCES orders (order_id),
  CONSTRAINT fk_returns_customer
    FOREIGN KEY (customer_id) REFERENCES customers (customer_id),
  CONSTRAINT chk_returns_refund
    CHECK (refund_amount >= 0)
) ENGINE = InnoDB;

SET FOREIGN_KEY_CHECKS = 1;

CREATE INDEX idx_addresses_customer ON addresses (customer_id);
CREATE INDEX idx_products_category_supplier ON products (category_id, supplier_id);
CREATE INDEX idx_inventory_warehouse_stock ON inventory (warehouse_id, quantity_on_hand);
CREATE INDEX idx_employees_warehouse ON employees (warehouse_id);
CREATE INDEX idx_orders_customer_date ON orders (customer_id, order_datetime);
CREATE INDEX idx_orders_status_date ON orders (order_status, order_datetime);
CREATE INDEX idx_orders_channel_date ON orders (sales_channel, order_datetime);
CREATE INDEX idx_order_items_order_product ON order_items (order_id, product_id);
CREATE INDEX idx_order_items_product ON order_items (product_id);
CREATE INDEX idx_payments_order_status ON payments (order_id, payment_status);
CREATE INDEX idx_shipments_order ON shipments (order_id);
CREATE INDEX idx_shipments_warehouse_carrier ON shipments (warehouse_id, carrier);
CREATE INDEX idx_reviews_product_rating ON reviews (product_id, rating);
CREATE INDEX idx_tickets_customer_status ON support_tickets (customer_id, ticket_status);
CREATE INDEX idx_tickets_topic_status ON support_tickets (topic, ticket_status);
CREATE INDEX idx_returns_order_status ON returns (order_id, return_status);

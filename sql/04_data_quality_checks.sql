-- Basic data quality checks for the RetailPulse dataset.
-- These checks are meant to catch obvious load issues before analysis.

USE retailpulse_analytics;

-- Row counts by table.
SELECT 'customers' AS table_name, COUNT(*) AS row_count FROM customers
UNION ALL SELECT 'addresses', COUNT(*) FROM addresses
UNION ALL SELECT 'categories', COUNT(*) FROM categories
UNION ALL SELECT 'suppliers', COUNT(*) FROM suppliers
UNION ALL SELECT 'products', COUNT(*) FROM products
UNION ALL SELECT 'warehouses', COUNT(*) FROM warehouses
UNION ALL SELECT 'inventory', COUNT(*) FROM inventory
UNION ALL SELECT 'employees', COUNT(*) FROM employees
UNION ALL SELECT 'orders', COUNT(*) FROM orders
UNION ALL SELECT 'order_items', COUNT(*) FROM order_items
UNION ALL SELECT 'payments', COUNT(*) FROM payments
UNION ALL SELECT 'shipments', COUNT(*) FROM shipments
UNION ALL SELECT 'reviews', COUNT(*) FROM reviews
UNION ALL SELECT 'support_tickets', COUNT(*) FROM support_tickets
UNION ALL SELECT 'returns', COUNT(*) FROM returns
ORDER BY table_name;

-- Order totals that do not tie back to subtotal, tax, and shipping.
-- In this dataset, subtotal is already net of line-item discounts.
SELECT
  order_id,
  subtotal,
  discount_amount,
  tax_amount,
  shipping_fee,
  total_amount,
  ROUND(subtotal + tax_amount + shipping_fee, 2) AS recalculated_total
FROM orders
WHERE ABS(total_amount - ROUND(subtotal + tax_amount + shipping_fee, 2)) > 0.01
LIMIT 50;

-- Paid payment rows that do not match the order total.
SELECT
  o.order_id,
  o.total_amount,
  SUM(p.amount) AS payment_amount,
  COUNT(*) AS payment_records
FROM orders AS o
INNER JOIN payments AS p
  ON p.order_id = o.order_id
  AND p.payment_status = 'paid'
GROUP BY
  o.order_id,
  o.total_amount
HAVING ABS(o.total_amount - SUM(p.amount)) > 0.01
LIMIT 50;

-- Shipments delivered before they were shipped.
SELECT
  shipment_id,
  order_id,
  shipped_datetime,
  delivered_datetime
FROM shipments
WHERE delivered_datetime IS NOT NULL
  AND delivered_datetime < shipped_datetime;

-- Reviews outside the expected 1-5 rating range.
SELECT
  review_id,
  rating
FROM reviews
WHERE rating NOT BETWEEN 1 AND 5;

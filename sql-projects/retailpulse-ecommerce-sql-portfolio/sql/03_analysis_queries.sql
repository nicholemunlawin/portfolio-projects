-- RetailPulse portfolio analysis queries.
-- These are grouped around business questions rather than SQL features.

USE retailpulse_analytics;

-- 1. Monthly revenue trend by sales channel.
SELECT
  DATE_FORMAT(order_datetime, '%Y-%m') AS order_month,
  sales_channel,
  COUNT(*) AS orders,
  ROUND(SUM(total_amount), 2) AS revenue,
  ROUND(AVG(total_amount), 2) AS avg_order_value
FROM orders
WHERE order_status IN ('shipped', 'delivered', 'refunded')
GROUP BY
  DATE_FORMAT(order_datetime, '%Y-%m'),
  sales_channel
ORDER BY
  order_month,
  revenue DESC;

-- 2. Top products by revenue and units sold.
SELECT
  p.product_id,
  p.product_name,
  c.category_name,
  SUM(oi.quantity) AS units_sold,
  ROUND(SUM(oi.line_total), 2) AS revenue
FROM order_items AS oi
INNER JOIN orders AS o
  ON o.order_id = oi.order_id
INNER JOIN products AS p
  ON p.product_id = oi.product_id
INNER JOIN categories AS c
  ON c.category_id = p.category_id
WHERE o.order_status IN ('shipped', 'delivered', 'refunded')
GROUP BY
  p.product_id,
  p.product_name,
  c.category_name
ORDER BY revenue DESC
LIMIT 20;

-- 3. Estimated category gross profit.
SELECT
  c.category_name,
  ROUND(SUM(oi.line_total), 2) AS revenue,
  ROUND(SUM(oi.quantity * p.unit_cost), 2) AS estimated_cost,
  ROUND(SUM(oi.line_total) - SUM(oi.quantity * p.unit_cost), 2) AS gross_profit,
  ROUND(
    (SUM(oi.line_total) - SUM(oi.quantity * p.unit_cost))
    / NULLIF(SUM(oi.line_total), 0) * 100,
    2
  ) AS gross_margin_pct
FROM order_items AS oi
INNER JOIN orders AS o
  ON o.order_id = oi.order_id
INNER JOIN products AS p
  ON p.product_id = oi.product_id
INNER JOIN categories AS c
  ON c.category_id = p.category_id
WHERE o.order_status IN ('shipped', 'delivered', 'refunded')
GROUP BY c.category_name
ORDER BY gross_profit DESC;

-- 4. Repeat purchase rate by acquisition channel.
WITH customer_order_counts AS (
  SELECT
    c.acquisition_channel,
    c.customer_id,
    COUNT(o.order_id) AS order_count
  FROM customers AS c
  LEFT JOIN orders AS o
    ON o.customer_id = c.customer_id
    AND o.order_status IN ('shipped', 'delivered', 'refunded')
  GROUP BY
    c.acquisition_channel,
    c.customer_id
)
SELECT
  acquisition_channel,
  COUNT(*) AS customers,
  SUM(order_count >= 2) AS repeat_customers,
  ROUND(SUM(order_count >= 2) / COUNT(*) * 100, 2) AS repeat_rate_pct
FROM customer_order_counts
GROUP BY acquisition_channel
ORDER BY repeat_rate_pct DESC;

-- 5. Highest-value customers.
SELECT
  c.customer_id,
  CONCAT(c.first_name, ' ', c.last_name) AS customer_name,
  c.customer_segment,
  COUNT(DISTINCT o.order_id) AS orders,
  ROUND(SUM(o.total_amount), 2) AS lifetime_value,
  DENSE_RANK() OVER (ORDER BY SUM(o.total_amount) DESC) AS value_rank
FROM customers AS c
INNER JOIN orders AS o
  ON o.customer_id = c.customer_id
WHERE o.order_status IN ('shipped', 'delivered', 'refunded')
GROUP BY
  c.customer_id,
  customer_name,
  c.customer_segment
ORDER BY lifetime_value DESC
LIMIT 25;

-- 6. RFM-style customer segmentation using the dataset's latest order date.
WITH analysis_date AS (
  SELECT DATE_ADD(DATE(MAX(order_datetime)), INTERVAL 1 DAY) AS as_of_date
  FROM orders
),
rfm AS (
  SELECT
    c.customer_id,
    DATEDIFF(ad.as_of_date, MAX(o.order_datetime)) AS recency_days,
    COUNT(DISTINCT o.order_id) AS frequency,
    SUM(o.total_amount) AS monetary
  FROM customers AS c
  INNER JOIN orders AS o
    ON o.customer_id = c.customer_id
  CROSS JOIN analysis_date AS ad
  WHERE o.order_status IN ('shipped', 'delivered', 'refunded')
  GROUP BY
    c.customer_id,
    ad.as_of_date
)
SELECT
  customer_id,
  recency_days,
  frequency,
  ROUND(monetary, 2) AS monetary,
  CASE
    WHEN recency_days <= 60 AND frequency >= 5 THEN 'Champions'
    WHEN recency_days <= 120 AND frequency >= 3 THEN 'Loyal'
    WHEN recency_days > 365 THEN 'Dormant'
    ELSE 'Developing'
  END AS rfm_segment
FROM rfm
ORDER BY monetary DESC
LIMIT 100;

-- 7. Delivery performance by carrier.
SELECT
  carrier,
  COUNT(*) AS delivered_shipments,
  ROUND(AVG(TIMESTAMPDIFF(HOUR, shipped_datetime, delivered_datetime)) / 24, 2) AS avg_delivery_days,
  ROUND(SUM(TIMESTAMPDIFF(HOUR, shipped_datetime, delivered_datetime) > 120) / COUNT(*) * 100, 2) AS pct_over_5_days
FROM shipments
WHERE delivered_datetime IS NOT NULL
GROUP BY carrier
ORDER BY avg_delivery_days;

-- 8. Warehouse inventory that is below reorder level.
SELECT
  w.warehouse_name,
  p.product_id,
  p.product_name,
  c.category_name,
  i.quantity_on_hand,
  i.reorder_level,
  i.reorder_level - i.quantity_on_hand AS units_below_reorder
FROM inventory AS i
INNER JOIN products AS p
  ON p.product_id = i.product_id
INNER JOIN categories AS c
  ON c.category_id = p.category_id
INNER JOIN warehouses AS w
  ON w.warehouse_id = i.warehouse_id
WHERE i.quantity_on_hand < i.reorder_level
ORDER BY
  units_below_reorder DESC,
  w.warehouse_name,
  p.product_name;

-- 9. Return rate by category.
WITH category_orders AS (
  SELECT DISTINCT
    c.category_name,
    o.order_id
  FROM orders AS o
  INNER JOIN order_items AS oi
    ON oi.order_id = o.order_id
  INNER JOIN products AS p
    ON p.product_id = oi.product_id
  INNER JOIN categories AS c
    ON c.category_id = p.category_id
  WHERE o.order_status IN ('delivered', 'refunded')
)
SELECT
  co.category_name,
  COUNT(DISTINCT co.order_id) AS fulfilled_orders,
  COUNT(DISTINCT r.return_id) AS returned_orders,
  ROUND(COUNT(DISTINCT r.return_id) / NULLIF(COUNT(DISTINCT co.order_id), 0) * 100, 2) AS return_rate_pct,
  ROUND(SUM(COALESCE(r.refund_amount, 0)), 2) AS refund_amount
FROM category_orders AS co
LEFT JOIN returns AS r
  ON r.order_id = co.order_id
GROUP BY co.category_name
ORDER BY return_rate_pct DESC;

-- 10. Support topics by resolution time.
SELECT
  topic,
  priority,
  COUNT(*) AS tickets,
  ROUND(
    AVG(
      CASE
        WHEN closed_datetime IS NOT NULL THEN TIMESTAMPDIFF(HOUR, opened_datetime, closed_datetime)
      END
    ),
    1
  ) AS avg_hours_to_close,
  ROUND(SUM(ticket_status IN ('open', 'pending_customer', 'escalated')) / COUNT(*) * 100, 2) AS active_ticket_pct
FROM support_tickets
GROUP BY
  topic,
  priority
ORDER BY
  avg_hours_to_close DESC,
  tickets DESC;

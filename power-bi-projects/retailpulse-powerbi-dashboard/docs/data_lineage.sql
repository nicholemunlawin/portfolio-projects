-- RetailPulse Power BI dashboard extract lineage.
-- Run after loading the companion MySQL project into retailpulse_analytics.

USE retailpulse_analytics;

-- kpi_summary.csv
SELECT
  COUNT(*) AS fulfilled_orders,
  ROUND(SUM(total_amount), 2) AS revenue,
  ROUND(AVG(total_amount), 2) AS avg_order_value,
  COUNT(DISTINCT customer_id) AS purchasing_customers,
  (SELECT COUNT(*) FROM returns) AS returns,
  ROUND((SELECT COUNT(*) FROM returns) / NULLIF(COUNT(*), 0) * 100, 2) AS return_rate_pct
FROM orders
WHERE order_status IN ('shipped', 'delivered', 'refunded');

-- sales_monthly_channel.csv
SELECT
  DATE_FORMAT(order_datetime, '%Y-%m-01') AS order_month,
  sales_channel,
  COUNT(*) AS orders,
  ROUND(SUM(total_amount), 2) AS revenue,
  ROUND(AVG(total_amount), 2) AS avg_order_value
FROM orders
WHERE order_status IN ('shipped', 'delivered', 'refunded')
GROUP BY
  DATE_FORMAT(order_datetime, '%Y-%m-01'),
  sales_channel
ORDER BY
  order_month,
  sales_channel;

-- product_performance.csv
SELECT
  p.product_id,
  p.product_name,
  c.category_name,
  p.brand,
  SUM(oi.quantity) AS units_sold,
  ROUND(SUM(oi.line_total), 2) AS revenue,
  ROUND(SUM(oi.quantity * p.unit_cost), 2) AS estimated_cost,
  ROUND(SUM(oi.line_total) - SUM(oi.quantity * p.unit_cost), 2) AS gross_profit
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
  c.category_name,
  p.brand
ORDER BY revenue DESC;

-- category_performance.csv
WITH category_sales AS (
  SELECT
    c.category_name,
    SUM(oi.quantity) AS units_sold,
    SUM(oi.line_total) AS revenue,
    SUM(oi.quantity * p.unit_cost) AS estimated_cost,
    COUNT(DISTINCT o.order_id) AS fulfilled_orders
  FROM order_items AS oi
  INNER JOIN orders AS o
    ON o.order_id = oi.order_id
  INNER JOIN products AS p
    ON p.product_id = oi.product_id
  INNER JOIN categories AS c
    ON c.category_id = p.category_id
  WHERE o.order_status IN ('shipped', 'delivered', 'refunded')
  GROUP BY c.category_name
),
category_returns AS (
  SELECT
    category_name,
    COUNT(DISTINCT return_id) AS returned_orders,
    SUM(refund_amount) AS refund_amount
  FROM (
    SELECT DISTINCT
      c.category_name,
      r.return_id,
      r.refund_amount
    FROM returns AS r
    INNER JOIN order_items AS oi
      ON oi.order_id = r.order_id
    INNER JOIN products AS p
      ON p.product_id = oi.product_id
    INNER JOIN categories AS c
      ON c.category_id = p.category_id
  ) AS category_return_orders
  GROUP BY category_name
)
SELECT
  cs.category_name,
  cs.units_sold,
  ROUND(cs.revenue, 2) AS revenue,
  ROUND(cs.revenue - cs.estimated_cost, 2) AS gross_profit,
  ROUND((cs.revenue - cs.estimated_cost) / NULLIF(cs.revenue, 0) * 100, 2) AS gross_margin_pct,
  cs.fulfilled_orders,
  COALESCE(cr.returned_orders, 0) AS returned_orders,
  ROUND(COALESCE(cr.returned_orders, 0) / NULLIF(cs.fulfilled_orders, 0) * 100, 2) AS return_rate_pct,
  ROUND(COALESCE(cr.refund_amount, 0), 2) AS refund_amount
FROM category_sales AS cs
LEFT JOIN category_returns AS cr
  ON cr.category_name = cs.category_name
ORDER BY gross_profit DESC;

-- customer_lifetime_value.csv
SELECT
  c.customer_id,
  CONCAT(c.first_name, ' ', c.last_name) AS customer_name,
  c.acquisition_channel,
  c.customer_segment,
  c.city,
  c.state,
  COUNT(o.order_id) AS orders,
  ROUND(SUM(o.total_amount), 2) AS lifetime_value,
  ROUND(AVG(o.total_amount), 2) AS avg_order_value,
  DATE(MAX(o.order_datetime)) AS last_order_date
FROM customers AS c
INNER JOIN orders AS o
  ON o.customer_id = c.customer_id
WHERE o.order_status IN ('shipped', 'delivered', 'refunded')
GROUP BY
  c.customer_id,
  customer_name,
  c.acquisition_channel,
  c.customer_segment,
  c.city,
  c.state
ORDER BY lifetime_value DESC;

-- customer_rfm_segments.csv
WITH analysis_date AS (
  SELECT DATE_ADD(DATE(MAX(order_datetime)), INTERVAL 1 DAY) AS as_of_date
  FROM orders
),
rfm AS (
  SELECT
    c.customer_id,
    c.acquisition_channel,
    c.customer_segment,
    DATEDIFF(ad.as_of_date, MAX(o.order_datetime)) AS recency_days,
    COUNT(o.order_id) AS frequency,
    SUM(o.total_amount) AS monetary
  FROM customers AS c
  INNER JOIN orders AS o
    ON o.customer_id = c.customer_id
  CROSS JOIN analysis_date AS ad
  WHERE o.order_status IN ('shipped', 'delivered', 'refunded')
  GROUP BY
    c.customer_id,
    c.acquisition_channel,
    c.customer_segment,
    ad.as_of_date
)
SELECT
  customer_id,
  acquisition_channel,
  customer_segment,
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
ORDER BY customer_id;

-- delivery_performance.csv
SELECT
  w.warehouse_name,
  s.carrier,
  s.shipping_method,
  COUNT(*) AS delivered_shipments,
  ROUND(AVG(TIMESTAMPDIFF(HOUR, s.shipped_datetime, s.delivered_datetime)) / 24, 2) AS avg_delivery_days,
  ROUND(SUM(TIMESTAMPDIFF(HOUR, s.shipped_datetime, s.delivered_datetime) > 120) / COUNT(*) * 100, 2) AS pct_over_5_days
FROM shipments AS s
INNER JOIN warehouses AS w
  ON w.warehouse_id = s.warehouse_id
WHERE s.delivered_datetime IS NOT NULL
GROUP BY
  w.warehouse_name,
  s.carrier,
  s.shipping_method
ORDER BY
  w.warehouse_name,
  s.carrier,
  s.shipping_method;

-- inventory_reorder.csv
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

-- support_resolution.csv
SELECT
  topic,
  priority,
  ticket_status,
  COUNT(*) AS tickets,
  SUM(closed_datetime IS NOT NULL) AS closed_tickets,
  ROUND(
    AVG(
      CASE
        WHEN closed_datetime IS NOT NULL
          THEN TIMESTAMPDIFF(HOUR, opened_datetime, closed_datetime)
      END
    ),
    1
  ) AS avg_hours_to_close
FROM support_tickets
GROUP BY
  topic,
  priority,
  ticket_status
ORDER BY
  topic,
  priority,
  ticket_status;

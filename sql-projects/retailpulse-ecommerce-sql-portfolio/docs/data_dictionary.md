# Data Dictionary

This is a quick reference for the CSV files and the MySQL tables created in `sql/01_schema.sql`.

| Table | Rows | Grain | Main Use |
|---|---:|---|---|
| `customers` | 10,000 | one row per customer | customer profile, signup, segment, and acquisition channel |
| `addresses` | 12,139 | one row per customer address | billing/shipping addresses |
| `categories` | 12 | one row per product category | product hierarchy |
| `suppliers` | 80 | one row per supplier | supplier lookup |
| `products` | 500 | one row per product | catalog, category, supplier, cost, and price |
| `warehouses` | 8 | one row per warehouse | fulfillment locations and capacity |
| `inventory` | 4,000 | one row per product per warehouse | stock on hand and reorder level |
| `employees` | 120 | one row per employee | sales, support, and operations staffing |
| `orders` | 50,000 | one row per order | order status, channel, customer, and total amount |
| `order_items` | 120,569 | one row per order line item | quantity, product, and line revenue |
| `payments` | 50,000 | one row per payment | payment method, status, amount, and timestamp |
| `shipments` | 42,526 | one row per shipment | carrier, warehouse, delivery timing, and shipment status |
| `reviews` | 14,478 | one row per review | product rating and review date |
| `support_tickets` | 12,088 | one row per support ticket | topic, priority, status, and resolution timing |
| `returns` | 3,399 | one row per return request | return status, reason, refund amount, and date |

## Key Relationships

- `customers.customer_id` connects to orders, addresses, reviews, support tickets, and returns.
- `orders.order_id` connects the order header to line items, payments, shipments, reviews, returns, and support tickets.
- `products.product_id` connects product details to order items, inventory, and reviews.
- `warehouses.warehouse_id` connects warehouses to inventory, shipments, and employees.
- `employees.employee_id` connects employees to sales-assisted orders and assigned support tickets.

## Column List

| Table | Columns |
|---|---|
| `customers` | `customer_id`, `first_name`, `last_name`, `email`, `acquisition_channel`, `customer_segment`, `city`, `state`, `signup_date`, `status` |
| `addresses` | `address_id`, `customer_id`, `address_type`, `street_address`, `city`, `state`, `postal_code`, `country`, `is_default` |
| `categories` | `category_id`, `category_name`, `description` |
| `suppliers` | `supplier_id`, `supplier_name`, `contact_email`, `city`, `state`, `country` |
| `products` | `product_id`, `product_name`, `category_id`, `supplier_id`, `brand`, `unit_cost`, `unit_price`, `status`, `created_date` |
| `warehouses` | `warehouse_id`, `warehouse_name`, `city`, `state`, `capacity_units` |
| `inventory` | `product_id`, `warehouse_id`, `quantity_on_hand`, `reorder_level`, `last_stock_check_date` |
| `employees` | `employee_id`, `first_name`, `last_name`, `department`, `job_title`, `warehouse_id`, `hire_date`, `status` |
| `orders` | `order_id`, `customer_id`, `order_datetime`, `order_status`, `sales_channel`, `subtotal`, `discount_amount`, `tax_amount`, `shipping_fee`, `total_amount`, `sales_rep_id` |
| `order_items` | `order_item_id`, `order_id`, `product_id`, `quantity`, `unit_price`, `discount_amount`, `line_total` |
| `payments` | `payment_id`, `order_id`, `payment_method`, `payment_status`, `amount`, `payment_datetime` |
| `shipments` | `shipment_id`, `order_id`, `warehouse_id`, `shipping_method`, `carrier`, `shipped_datetime`, `delivered_datetime`, `shipment_status` |
| `reviews` | `review_id`, `customer_id`, `product_id`, `order_id`, `rating`, `review_text`, `review_date` |
| `support_tickets` | `ticket_id`, `customer_id`, `order_id`, `topic`, `ticket_status`, `priority`, `opened_datetime`, `closed_datetime`, `assigned_employee_id` |
| `returns` | `return_id`, `order_id`, `customer_id`, `return_reason`, `return_status`, `refund_amount`, `return_date` |

# Dashboard Data Dictionary

These are the CSV files I used in the Power BI report. They come from the `retailpulse_analytics` MySQL database in my [RetailPulse SQL portfolio project](../../../sql-projects/retailpulse-ecommerce-sql-portfolio).

I kept these tables denormalized because the dashboard does not need the full source model. It only needs the summary tables behind the visuals and measures.

## Extracts

| File | Rows | Grain | Where I used it |
|---|---:|---|---|
| `kpi_summary.csv` | 1 | overall dashboard summary | executive KPI cards |
| `sales_monthly_channel.csv` | 180 | one row per month and sales channel | revenue and order trend visuals |
| `product_performance.csv` | 500 | one row per product | product ranking and profitability |
| `category_performance.csv` | 12 | one row per category | category margin and return analysis |
| `customer_lifetime_value.csv` | 9,854 | one row per purchasing customer | customer value analysis |
| `customer_rfm_segments.csv` | 9,854 | one row per purchasing customer | RFM segmentation |
| `delivery_performance.csv` | 128 | one row per warehouse, carrier, and shipping method | delivery operations |
| `inventory_reorder.csv` | 288 | one row per product and warehouse below reorder level | inventory risk |
| `support_resolution.csv` | 160 | one row per topic, priority, and ticket status | support operations |

## Columns

### `kpi_summary.csv`

| Column | Definition |
|---|---|
| `fulfilled_orders` | Count of orders with status `shipped`, `delivered`, or `refunded` |
| `revenue` | Sum of `orders.total_amount` for fulfilled orders |
| `avg_order_value` | Revenue divided by fulfilled orders |
| `purchasing_customers` | Distinct customers with at least one fulfilled order |
| `returns` | Count of return records |
| `return_rate_pct` | Returns divided by fulfilled orders |

### `sales_monthly_channel.csv`

| Column | Definition |
|---|---|
| `order_month` | First day of the order month |
| `sales_channel` | Sales channel from the order header |
| `orders` | Fulfilled order count |
| `revenue` | Fulfilled order revenue |
| `avg_order_value` | Revenue divided by orders |

### `product_performance.csv`

| Column | Definition |
|---|---|
| `product_id` | Product identifier |
| `product_name` | Product display name |
| `category_name` | Product category |
| `brand` | Product brand |
| `units_sold` | Sum of fulfilled order item quantities |
| `revenue` | Sum of fulfilled order item line totals |
| `estimated_cost` | Sum of quantity multiplied by product unit cost |
| `gross_profit` | Revenue minus estimated cost |

### `category_performance.csv`

| Column | Definition |
|---|---|
| `category_name` | Product category |
| `units_sold` | Sum of fulfilled order item quantities |
| `revenue` | Sum of fulfilled order item line totals |
| `gross_profit` | Revenue minus estimated cost |
| `gross_margin_pct` | Gross profit divided by revenue |
| `fulfilled_orders` | Distinct fulfilled orders containing the category |
| `returned_orders` | Distinct returned orders containing the category |
| `return_rate_pct` | Returned orders divided by fulfilled orders |
| `refund_amount` | Refund amount tied to returned orders in the category |

### `customer_lifetime_value.csv`

| Column | Definition |
|---|---|
| `customer_id` | Customer identifier |
| `customer_name` | Customer first and last name from the source data |
| `acquisition_channel` | Customer acquisition channel |
| `customer_segment` | Customer segment from the source data |
| `city` | Customer city |
| `state` | Customer state |
| `orders` | Fulfilled order count |
| `lifetime_value` | Sum of fulfilled order totals |
| `avg_order_value` | Lifetime value divided by orders |
| `last_order_date` | Most recent fulfilled order date |

### `customer_rfm_segments.csv`

| Column | Definition |
|---|---|
| `customer_id` | Customer identifier |
| `acquisition_channel` | Customer acquisition channel |
| `customer_segment` | Customer segment from the source data |
| `recency_days` | Days between the analysis date and the customer's latest fulfilled order |
| `frequency` | Fulfilled order count |
| `monetary` | Sum of fulfilled order totals |
| `rfm_segment` | RFM group assigned with my SQL rules: Champions, Loyal, Dormant, or Developing |

### `delivery_performance.csv`

| Column | Definition |
|---|---|
| `warehouse_name` | Fulfillment warehouse |
| `carrier` | Shipment carrier |
| `shipping_method` | Shipping method |
| `delivered_shipments` | Count of shipments with a delivered timestamp |
| `avg_delivery_days` | Average shipped-to-delivered duration in days |
| `pct_over_5_days` | Share of delivered shipments taking more than five days |

### `inventory_reorder.csv`

| Column | Definition |
|---|---|
| `warehouse_name` | Warehouse holding the inventory |
| `product_id` | Product identifier |
| `product_name` | Product display name |
| `category_name` | Product category |
| `quantity_on_hand` | Current inventory count |
| `reorder_level` | Reorder threshold |
| `units_below_reorder` | Reorder level minus quantity on hand |

### `support_resolution.csv`

| Column | Definition |
|---|---|
| `topic` | Support ticket topic |
| `priority` | Ticket priority |
| `ticket_status` | Ticket status |
| `tickets` | Ticket count |
| `closed_tickets` | Tickets with a closed timestamp |
| `avg_hours_to_close` | Average opened-to-closed duration in hours for tickets with a closed timestamp |

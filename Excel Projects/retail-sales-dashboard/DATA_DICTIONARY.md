# Data Dictionary

## Workbook Sheets

| Sheet | Range | Purpose |
|---|---:|---|
| `Dashboard` | `A1:W23` | Main retail sales and customer experience dashboard. |
| `Analysis` | `A1:D15` | Business questions, insights, implications, and suggested actions. |
| `Sales_Data` | `A1:Z501` | Order-level source dataset. |
| `Lookup_Lists` | `A1:Z6` | Lookup values for categories, margins, segments, regions, channels, payment methods, and return status. |
| `Sales and Profit by Category` | `A3:D32` | Supporting summary and chart data by product category. |
| `Sales and Profit by Region` | `A3:C8` | Supporting summary and chart data by region. |
| `Monthly Sales and Profit Trend` | `A3:J39` | Supporting monthly trend summary and chart data. |

## Sales_Data Fields

| Field | Description |
|---|---|
| `Order_ID` | Unique order identifier. |
| `Order_Date` | Order date stored as an Excel date serial. |
| `Ship_Date` | Ship date stored as an Excel date serial. |
| `Customer_ID` | Unique customer identifier. |
| `Customer_Segment` | Customer segment category. |
| `Country` | Country for the order. |
| `Region` | Sales region. |
| `City` | Customer or order city. |
| `Product_Category` | Product category. |
| `Product_Subcategory` | Product subcategory. |
| `Product_Name` | Product name. |
| `Channel` | Sales channel. |
| `Payment_Method` | Payment method used for the order. |
| `Quantity` | Number of units ordered. |
| `Unit_Price` | Price per unit. |
| `Discount` | Discount applied to the order. |
| `Shipping_Cost` | Shipping cost for the order. |
| `Sales` | Sales amount. |
| `Profit` | Profit amount. |
| `Returned` | Return status. |
| `Rating` | Customer rating value. |
| `Delivery_Days` | Delivery duration in days. |
| `Return_Value` | Monetary value associated with returns. |

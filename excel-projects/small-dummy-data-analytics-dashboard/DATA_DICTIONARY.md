# Data Dictionary

## Workbook Sheets

| Sheet | Range | Purpose |
|---|---:|---|
| `Dashboard` | `A1:W19` | Main dashboard for the compact sample dataset. |
| `Analysis` | `A1:D14` | Business questions, insights, implications, and suggested actions. |
| `Transactions` | `A1:R101` | Transaction-level source dataset. |
| `Customers` | `A1:F21` | Customer reference table. |
| `Analyze` | `B3:H57` | Supporting summaries and visual elements. |
| `Products` | `A1:E16` | Product reference table. |

## Transactions Fields

| Field | Description |
|---|---|
| `Order ID` | Unique order identifier. |
| `Order Date` | Order date stored as an Excel date serial. |
| `Customer ID` | Customer identifier linking to the `Customers` sheet. |
| `Product ID` | Product identifier linking to the `Products` sheet. |
| `Sales Channel` | Channel used for the sale. |
| `Payment Method` | Payment method used by the customer. |
| `Quantity` | Number of units sold. |
| `Unit Price` | Price per unit. |
| `Discount %` | Discount rate applied to the order. |
| `Shipping Fee` | Shipping charge for the order. |
| `Gross Sales` | Sales before discount adjustments. |
| `Discount Amount` | Discount value applied to the order. |
| `Net Sales` | Sales after discount and adjustments. |
| `Unit Cost` | Product cost per unit. |
| `Total Cost` | Total cost for the transaction. |
| `Profit` | Transaction profit. |
| `Order Status` | Status of the order, such as completed, returned, or cancelled. |
| `Satisfaction Score` | Customer satisfaction score. |

## Customers Fields

| Field | Description |
|---|---|
| `Customer ID` | Unique customer identifier. |
| `Customer Name` | Customer display name. |
| `Segment` | Customer segment. |
| `Region` | Customer region. |
| `City` | Customer city. |
| `Signup Date` | Signup date stored as an Excel date serial. |

## Products Fields

| Field | Description |
|---|---|
| `Product ID` | Unique product identifier. |
| `Product Name` | Product display name. |
| `Category` | Product category. |
| `Unit Cost` | Cost per unit. |
| `List Price` | Standard selling price. |

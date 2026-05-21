# Retail Sales Dashboard

Excel dashboard project for retail sales, profit, returns, customer experience, product category performance, regional performance, channels, and monthly trends.

![Retail Sales Dashboard](<Retail Sales Analytics (Dashboard) Capture.png>)

## Files

| File | Purpose |
|---|---|
| `Retail Sales Analytics (Dashboard).xlsx` | Main Excel workbook containing the dashboard, sales source data, analysis, lookup lists, and supporting summary sheets. |
| `Retail Sales Analytics (Dashboard) Capture.png` | Dashboard preview image for GitHub. |
| `DATA_DICTIONARY.md` | Sheet catalog and key field descriptions. |
| `.gitignore` | Excludes local Excel lock files, OS files, editor folders, and generated exports. |
| `.gitattributes` | Marks workbook and image assets as binary files. |

## Workbook Structure

| Sheet | Purpose |
|---|---|
| `Dashboard` | Main visual dashboard. |
| `Analysis` | Business questions, insights, implications, and suggested actions. |
| `Sales_Data` | Order-level source dataset. |
| `Lookup_Lists` | Lookup values for categories and controlled fields. |
| `Sales and Profit by Category` | Supporting summary and chart data by product category. |
| `Sales and Profit by Region` | Supporting summary and chart data by region. |
| `Monthly Sales and Profit Trend` | Supporting monthly trend summary and chart data. |

## Project Write-Up

### Selected Analysis Highlights

| Business question | Insight | Implication | Suggested action |
|---|---|---|---|
| How is the business performing overall? | Performance is strong but uneven across categories, regions, and months. | Revenue and profit are led by Electronics and the East region, while Office Supplies, North returns, and softer months create avoidable performance drag. | Protect the strongest profit drivers while fixing underperforming categories, high-return regions, and weaker months through targeted pricing, operations, and promotion actions. |
| Which product category is driving most revenue and profit? | Electronics is the top-performing category. | Electronics generated the highest sales, about PHP 5.73M, and the highest profit, about PHP 852.9K. | Increase inventory, prioritize marketing spend, and identify the best-selling electronics items to scale further. |
| Which category needs pricing, cost, or demand review? | Office Supplies is losing money. | Office Supplies had low sales, about PHP 126K, and a negative profit of about -PHP 17.7K. | Review supplier costs, pricing, discounts, and product mix. Consider reducing low-margin items or bundling them with stronger categories. |
| Which region should be used as a benchmark for strong performance? | East is the best-performing region. | East had the highest sales, highest profit, and the lowest return rate at 3.7%. | Study East's sales strategy, customer service process, and fulfillment practices, then apply the best practices to other regions. |
| Where should we investigate customer dissatisfaction, product issues, or fulfillment problems? | North has the highest return rate. | North's return rate is 5.3%, higher than other regions. | Check return reasons, delivery issues, product quality, and customer feedback in the North region. Focus on reducing avoidable returns. |

### The Dataset

This project uses a synthetically generated retail sales and customer experience dataset included directly in the workbook on the `Sales_Data` sheet. The dataset contains fictional order-level records with order dates, shipping dates, customer segments, regions, cities, product categories, product names, sales channels, payment methods, sales, profit, return status, delivery days, and customer ratings. It does not contain real customer, company, transaction, or personally identifiable information, and is safe to publish publicly. No external data connection is required.

### Methodology & Cleaning

The workbook prepares order-level retail data into dashboard-ready summaries by category, region, and month. Lookup lists are used to keep categories, customer segments, regions, channels, payment methods, and return values consistent. The model separates dates, categorical fields, quantities, prices, discounts, shipping costs, sales, profit, return values, and ratings into structured columns. Typical preparation steps for this workbook include removing duplicate order IDs, standardizing text with `TRIM` and `PROPER`, formatting dates consistently, validating categories against lookup lists, and building summary tables and pivot-table outputs for dashboard reporting.

### Formulas & Functions

Advanced Excel features used in this workbook include Excel tables, pivot tables, dashboard charts, lookup lists, and calculated fields. Formula patterns found in the workbook include `XLOOKUP`, `COUNTIF`, `COUNTIFS`, and `IF`.

## How to Use

1. Download or clone this repository.
2. Open `Retail Sales Analytics (Dashboard).xlsx` in Microsoft Excel.
3. Start with the `Dashboard` sheet for the visual summary.
4. Review `Analysis` for business interpretation and recommended actions.
5. Use `Sales_Data` and the supporting summary sheets for validation or deeper exploration.

## Data Notes

- The workbook includes its own sample source data.
- No external data connection is required based on the included workbook structure.
- Dates may appear as Excel serial dates when inspected outside Excel.

## License

This project is licensed under the [Creative Commons Attribution 4.0 International License](LICENSE), allowing reuse and adaptation with attribution.

# Small Dummy Data Dashboard

Compact Excel dashboard project using sample retail-style data across transactions, customers, and products.

![Small Dummy Data Dashboard](<Small Dummy Data Analytics (Dashboard) Capture.png>)

## Files

| File | Purpose |
|---|---|
| `Small Dummy Data Analytics (Dashboard).xlsx` | Main Excel workbook containing the dashboard, analysis, transactions, customers, products, and supporting summaries. |
| `Small Dummy Data Analytics (Dashboard) Capture.png` | Dashboard preview image for GitHub. |
| `DATA_DICTIONARY.md` | Sheet catalog and key field descriptions. |
| `.gitignore` | Excludes local Excel lock files, OS files, editor folders, and generated exports. |
| `.gitattributes` | Marks workbook and image assets as binary files. |

## Workbook Structure

| Sheet | Purpose |
|---|---|
| `Dashboard` | Main visual dashboard. |
| `Analysis` | Business questions, insights, implications, and suggested actions. |
| `Transactions` | Transaction-level source dataset. |
| `Customers` | Customer reference table. |
| `Analyze` | Supporting summaries and visual elements. |
| `Products` | Product reference table. |

## Project Write-Up

### Selected Analysis Highlights

| Business question | Insight | Implication | Suggested action |
|---|---|---|---|
| How is the business performing overall? | Dashboard shows total sales of 277,677 and profit of 114,402, a 41.2% profit margin. Completed orders are 60%, returned orders 21%, cancelled orders 19%, and average satisfaction is 2.88 / 5. | Profitability is strong, but 40% of orders not completing cleanly and a below-neutral satisfaction score create meaningful leakage risk. | Prioritize reducing returns and cancellations while investigating satisfaction drivers by product, region, and fulfillment step. |
| Which region leads sales? | North leads with 82,149 sales and 34,104 profit, or 29.6% of total sales. Central is close behind with 80,334 sales and 34,164 profit. | Revenue is concentrated in North and Central, suggesting these markets have the strongest current demand and execution. | Protect stock availability and service levels in North/Central, then replicate their channel or promotion playbook in lower-performing regions. |
| Which category drives revenue? | Electronics generates 187,857 sales and 72,967 profit, representing 67.7% of total sales. | The business is highly dependent on Electronics, creating concentration risk if demand, inventory, or supplier economics shift. | Maintain Electronics availability and campaigns, but diversify growth into profitable non-Electronics categories. |
| Are order outcomes healthy? | Only 60% of orders are completed, while 21% are returned and 19% are cancelled. | A 40% non-completion rate suggests substantial revenue leakage and possible customer experience issues. | Set a near-term target to lift completed orders above 75% by reducing top cancellation and return causes. |
| What is the highest-priority growth lever? | The clearest opportunity is to improve South-region performance, grow high-margin non-Electronics categories, and reduce order leakage. | These three levers can improve both revenue resilience and profitability without relying only on Electronics growth. | Launch a 90-day action plan with KPIs for South sales, non-Electronics mix, completion rate, return rate, cancellation rate, and satisfaction. |

### The Dataset

This project uses a compact synthetically generated sample dataset included directly in the workbook across the `Transactions`, `Customers`, and `Products` sheets. The dataset represents fictional retail-style transactions linked to customer and product reference tables, including order dates, customers, products, channels, payment methods, quantities, prices, discounts, costs, profit, order status, and satisfaction scores. It does not contain real customer, company, transaction, or personally identifiable information, and is safe to publish publicly. No external data connection is required.

### Methodology & Cleaning

The workbook structures the dataset into separate fact and lookup-style sheets: transaction records, customer records, and product records. This makes the data easier to validate, summarize, and analyze. The dashboard and analysis sheets use cleaned transaction fields and supporting summaries to report sales, profit, return rate, order status, satisfaction, region performance, and product category performance. Typical preparation steps for this workbook include removing duplicate order IDs, standardizing customer and product IDs, cleaning text with `TRIM` and `PROPER`, formatting dates consistently, checking numeric fields such as quantity, price, discount, cost, and profit, and using the customer and product sheets as controlled reference tables.

### Formulas & Functions

Advanced Excel features used in this workbook include Excel tables, pivot tables, dashboard charts, customer and product reference tables, and summary calculations. Formula patterns found in the workbook include `AVERAGEIF`, along with pivot-table based aggregation for sales, profit, returns, satisfaction, regions, and categories.

## How to Use

1. Download or clone this repository.
2. Open `Small Dummy Data Analytics (Dashboard).xlsx` in Microsoft Excel.
3. Start with the `Dashboard` sheet for the visual summary.
4. Review `Analysis` for business interpretation and recommended actions.
5. Use `Transactions`, `Customers`, and `Products` for validation or deeper exploration.

## Data Notes

- The workbook includes its own sample source data.
- No external data connection is required based on the included workbook structure.
- Dates may appear as Excel serial dates when inspected outside Excel.

## License

This project is licensed under the [Creative Commons Attribution 4.0 International License](LICENSE), allowing reuse and adaptation with attribution.

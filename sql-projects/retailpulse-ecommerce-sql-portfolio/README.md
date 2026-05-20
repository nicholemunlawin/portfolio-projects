# RetailPulse Ecommerce SQL Portfolio

RetailPulse is a MySQL portfolio project built around a synthetic ecommerce dataset. I use it to practice the kind of SQL work I would expect in a retail analytics role: revenue reporting, product performance, customer behavior, inventory checks, shipping performance, returns, and support operations.

The project is intentionally structured like a small analytics repo instead of a one-off SQL script. The raw CSVs are included, the schema is normalized, and the analysis queries are grouped around business questions.

## Repo Structure

```text
.
|-- data/                         # CSV source files
|-- docs/
|   |-- data_dictionary.md         # table summaries and grain
|   |-- erd.md                     # Mermaid ERD
|   `-- project_brief.md           # analysis plan and portfolio angle
|-- sql/
|   |-- 01_schema.sql              # database, tables, keys, indexes
|   |-- 02_load_data.sql           # LOAD DATA LOCAL INFILE imports
|   |-- 03_analysis_queries.sql    # portfolio analysis queries
|   `-- 04_data_quality_checks.sql # basic validation checks
`-- README.md
```

## Dataset Snapshot

| Area | Tables | Notes |
|---|---|---|
| Customers | `customers`, `addresses` | customer profile, signup, location, and address data |
| Sales | `orders`, `order_items`, `payments` | order headers, line items, payment status, and revenue fields |
| Products | `products`, `categories`, `suppliers` | product catalog, cost, price, category, and supplier attributes |
| Operations | `warehouses`, `inventory`, `shipments` | stock levels and delivery performance |
| Experience | `reviews`, `support_tickets`, `returns` | product feedback, support cases, return/refund activity |

Total analytics rows, excluding headers and `data_dictionary.csv`: **319,919**.

## Tools Used

- MySQL 8+
- SQL features: joins, CTEs, window functions, conditional aggregation, date logic, and indexes
- GitHub Markdown with Mermaid for the ERD

## How To Run

Run these commands from the project root.

For Git Bash, Command Prompt, or macOS/Linux shells:

```bash
mysql -u root -p < sql/01_schema.sql
```

For Windows PowerShell:

```powershell
mysql -u root -p --execute "SOURCE sql/01_schema.sql"
```

If local file loading is disabled, enable it once with an admin MySQL user:

```sql
SET GLOBAL local_infile = 1;
```

Then import the CSV files:

For Git Bash, Command Prompt, or macOS/Linux shells:

```bash
mysql --local-infile=1 -u root -p retailpulse_analytics < sql/02_load_data.sql
```

For Windows PowerShell:

```powershell
mysql --local-infile=1 -u root -p retailpulse_analytics --execute "SOURCE sql/02_load_data.sql"
```

After loading the data, I usually run the checks first:

For Git Bash, Command Prompt, or macOS/Linux shells:

```bash
mysql -u root -p retailpulse_analytics < sql/04_data_quality_checks.sql
```

For Windows PowerShell:

```powershell
mysql -u root -p retailpulse_analytics --execute "SOURCE sql/04_data_quality_checks.sql"
```

Then run the analysis file.

For Git Bash, Command Prompt, or macOS/Linux shells:

```bash
mysql -u root -p retailpulse_analytics < sql/03_analysis_queries.sql
```

For Windows PowerShell:

```powershell
mysql -u root -p retailpulse_analytics --execute "SOURCE sql/03_analysis_queries.sql"
```

## Business Questions

The main questions I built the SQL around:

- Which months and sales channels are driving revenue?
- Which products and categories contribute the most gross profit?
- Which acquisition channels bring in customers who purchase again?
- Who are the highest-value customers?
- Where are shipments taking longer than expected?
- Which products or categories are tied to more returns?
- Which inventory items need attention?
- Which support topics take the longest to resolve?

## Notes

The data is synthetic, so the project is safe to publish. I kept the analysis focused on repeatable SQL patterns instead of making unsupported claims about a real company.

For more detail, see [the project brief](docs/project_brief.md), [data dictionary](docs/data_dictionary.md), and [ERD](docs/erd.md).

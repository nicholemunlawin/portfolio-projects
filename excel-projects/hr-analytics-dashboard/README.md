# HR Analytics Dashboard

Excel dashboard project for workforce analytics, attrition monitoring, employee demographics, compensation, tenure, engagement, and performance insights.

![HR Analytics Dashboard](<HR Analytics (Dashboard) Capture.png>)

## Files

| File | Purpose |
|---|---|
| `HR Analytics (Dashboard).xlsx` | Main Excel workbook containing the dashboard, analysis, employee source data, metrics, and lookup lists. |
| `HR Analytics (Dashboard) Capture.png` | Dashboard preview image for GitHub. |
| `DATA_DICTIONARY.md` | Sheet catalog and key field descriptions. |
| `.gitignore` | Excludes local Excel lock files, OS files, editor folders, and generated exports. |
| `.gitattributes` | Marks workbook and image assets as binary files. |

## Workbook Structure

| Sheet | Purpose |
|---|---|
| `Dashboard` | Main visual dashboard. |
| `Analysis` | Business questions, insights, implications, and suggested actions. |
| `Employee_Data` | Employee-level source dataset. |
| `Metrics` | Calculated metrics used by the dashboard. |
| `Lookup_Lists` | Lookup values used for controlled categories. |

## Project Write-Up

### The Dataset

This project uses a synthetically generated HR analytics dataset included directly in the workbook on the `Employee_Data` sheet. The data represents fictional employee records across departments, job levels, locations, salary, tenure, performance, engagement, training, overtime, absence, promotion, and attrition fields. It does not contain real employee, company, or personally identifiable information, and is safe to publish publicly. No external data connection is required.

### Methodology & Cleaning

The workbook organizes employee-level records into dashboard-ready metrics and summary views. The data was prepared into consistent tabular fields, with standardized categorical values for departments, job levels, locations, employment types, and lookup lists. Date fields are stored in Excel date format, numeric measures are separated into dedicated columns, and the dashboard uses the cleaned source table to calculate workforce KPIs, attrition measures, average salary, average tenure, engagement, and department-level summaries. Typical Excel preparation steps for this workbook include removing duplicate employee IDs, standardizing text formats with `TRIM` and `PROPER`, validating categories against lookup lists, and keeping blank termination dates for active employees.

### Formulas & Functions

Advanced Excel features used in this workbook include Excel tables, KPI summary formulas, dashboard charts, and dynamic summary calculations. Formula patterns found in the workbook include `COUNTIF`, `COUNTIFS`, `SUM`, `SUMIF`, `AVERAGE`, `AVERAGEIF`, `COUNTA`, `IFERROR`, and `UNIQUE`.

## How to Use

1. Download or clone this repository.
2. Open `HR Analytics (Dashboard).xlsx` in Microsoft Excel.
3. Start with the `Dashboard` sheet for the visual summary.
4. Review `Analysis` for business interpretation and recommended actions.
5. Use `Employee_Data` and `Metrics` for validation or deeper exploration.

## Data Notes

- The workbook includes its own sample source data.
- No external data connection is required based on the included workbook structure.
- Dates may appear as Excel serial dates when inspected outside Excel.

## License

This project is licensed under the [Creative Commons Attribution 4.0 International License](LICENSE), allowing reuse and adaptation with attribution.

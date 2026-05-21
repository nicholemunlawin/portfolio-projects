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

### Selected Analysis Highlights

| Business question | Insight | Implication | Suggested action |
|---|---|---|---|
| How healthy is the overall workforce base? | Total headcount is 700, with 628 active employees, 10.3% attrition, 3.5 engagement, and 56.0 months average tenure. | The workforce is sizeable and mostly active, but the current attrition level still creates a meaningful retention-management need. | Track attrition and engagement monthly; set a target threshold and review movement by department and role level. |
| Where is retention risk most concentrated by department? | Engineering has the highest department attrition at 15.0% with 23 terminations. | The highest-risk department combines a high attrition rate with meaningful headcount impact, so improvements there can materially reduce overall turnover. | Prioritize exit-interview themes, manager check-ins, and retention actions for the highest-attrition department. |
| Which departments appear to be retention strengths? | Marketing has the lowest department attrition at 5.0%. | Low-attrition teams may have practices, manager behaviors, or work-design conditions worth replicating elsewhere. | Interview leaders in the lowest-attrition departments and translate their practices into repeatable retention playbooks. |
| Is attrition concentrated by job level? | Senior has the highest job-level attrition at 11.6% vs. overall attrition of 10.3%. | Attrition at specific levels can signal career-path, compensation, manager-readiness, or workload issues that averages hide. | Review promotion velocity, compensation competitiveness, and manager support for the highest-attrition job level. |
| What does tenure suggest about turnover timing? | Terminated employees average 25.3 months tenure vs. 59.5 months for active employees. | Departures are occurring much earlier than the tenure profile of active employees, highlighting an early/mid-tenure retention window. | Strengthen onboarding, first-year career conversations, stay interviews, and 24-month retention checkpoints. |

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

# Data Model

## Model Setup
I kept this as a simple single-table Power BI model because the source data is one survey table.

## Source Table
`Data Professional Survey`

The table comes from `data/Data Professional Survey.xlsx`. I also exported the same data as `data/sample_data.csv` so it is easier to preview on GitHub.

## Grain
Each row represents one anonymous survey response.

## Size
- Rows: 630
- Source columns: 28

## Main Identifier
`Unique ID`

Each survey response has its own unique ID. The `Email` column does not contain real email addresses in this file; every value is listed as `anonymous`.

## Main Fields I Used
- `Q1 - Which Title Best Fits your Current Role?`
- `Q2 - Did you switch careers into Data?`
- `Q3 - Current Yearly Salary (in USD)`
- `Q4 - What Industry do you work in?`
- `Q5 - Favorite Programming Language`
- `Q6 - How Happy are you in your Current Position with the following? (Salary)`
- `Q6 - How Happy are you in your Current Position with the following? (Work/Life Balance)`
- `Q6 - How Happy are you in your Current Position with the following? (Coworkers)`
- `Q6 - How Happy are you in your Current Position with the following? (Management)`
- `Q6 - How Happy are you in your Current Position with the following? (Upward Mobility)`
- `Q6 - How Happy are you in your Current Position with the following? (Learning New Things)`
- `Q7 - How difficult was it for you to break into Data?`
- `Q8 - If you were to look for a new job today, what would be the most important thing to you?`
- `Q9 - Male/Female?`
- `Q10 - Current Age`
- `Q11 - Which Country do you live in?`
- `Q12 - Highest Level of Education`
- `Q13 - Ethnicity`

## Power BI Transformations
The PBIX report references an `Average Salary` field. That field is not in the raw Excel workbook, so I used a transformed salary value inside Power BI based on `Q3 - Current Yearly Salary (in USD)` which was done through Power Query.

## Relationships
There are no separate dimension tables in this project folder. The dashboard works from one imported survey table instead of a star schema.


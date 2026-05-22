# Data Dictionary

I created this data dictionary to make the survey fields easier to review before opening the Power BI file. The table below keeps the original column names from the source workbook and adds a short note about how each field is used or what it contains.

Source workbook: `Data Professional Survey.xlsx`  
Sheet: `Data Professional Survey`  
Rows: 630  
Columns: 28

## Field Summary

| Column | Type In Source Extract | Non-Null | Missing | Unique Values | Description |
|---|---:|---:|---:|---:|---|
| `Unique ID` | Text | 630 | 0 | 630 | Anonymous unique survey response identifier. |
| `Email` | Text | 630 | 0 | 1 | Email field; all provided values are `anonymous`. |
| `Date Taken (America/New_York)` | Text/date | 630 | 0 | 16 | Date when the survey response was submitted. |
| `Time Taken (America/New_York)` | Text/time | 630 | 0 | 453 | Time when the survey response was submitted. |
| `Browser` | Blank | 0 | 630 | 0 | Browser metadata column; no values are available in the provided file. |
| `OS` | Blank | 0 | 630 | 0 | Operating system metadata column; no values are available in the provided file. |
| `City` | Blank | 0 | 630 | 0 | City metadata column; no values are available in the provided file. |
| `Country` | Blank | 0 | 630 | 0 | Country metadata column; no values are available in the provided file. Use `Q11` for respondent country. |
| `Referrer` | Blank | 0 | 630 | 0 | Referrer metadata column; no values are available in the provided file. |
| `Time Spent` | Text/duration | 630 | 0 | 203 | Time spent completing the survey. |
| `Q1 - Which Title Best Fits your Current Role?` | Text | 630 | 0 | 83 | Respondent's current or closest data role. |
| `Q2 - Did you switch careers into Data?` | Text | 630 | 0 | 2 | Whether the respondent switched careers into data. |
| `Q3 - Current Yearly Salary (in USD)` | Text/category | 630 | 0 | 8 | Salary band selected by the respondent. |
| `Q4 - What Industry do you work in?` | Text | 630 | 0 | 146 | Respondent's industry. |
| `Q5 - Favorite Programming Language` | Text | 630 | 0 | 43 | Respondent's favorite programming language. |
| `Q6 - How Happy are you in your Current Position with the following? (Salary)` | Number | 623 | 7 | 11 | Salary satisfaction score. |
| `Q6 - How Happy are you in your Current Position with the following? (Work/Life Balance)` | Number | 620 | 10 | 11 | Work-life balance satisfaction score. |
| `Q6 - How Happy are you in your Current Position with the following? (Coworkers)` | Number | 619 | 11 | 11 | Coworker satisfaction score. |
| `Q6 - How Happy are you in your Current Position with the following? (Management)` | Number | 618 | 12 | 11 | Management satisfaction score. |
| `Q6 - How Happy are you in your Current Position with the following? (Upward Mobility)` | Number | 617 | 13 | 11 | Upward mobility satisfaction score. |
| `Q6 - How Happy are you in your Current Position with the following? (Learning New Things)` | Number | 625 | 5 | 11 | Learning opportunity satisfaction score. |
| `Q7 - How difficult was it for you to break into Data?` | Text/category | 630 | 0 | 5 | Respondent's perceived difficulty entering the data field. |
| `Q8 - If you were to look for a new job today, what would be the most important thing to you?` | Text/category | 630 | 0 | 39 | Most important job-search priority. |
| `Q9 - Male/Female?` | Text/category | 630 | 0 | 2 | Gender category as provided in the source survey. |
| `Q10 - Current Age` | Number | 630 | 0 | 41 | Respondent age. |
| `Q11 - Which Country do you live in?` | Text | 630 | 0 | 98 | Respondent country of residence. |
| `Q12 - Highest Level of Education` | Text/category | 578 | 52 | 5 | Highest education level selected by respondent. |
| `Q13 - Ethnicity` | Text/category | 630 | 0 | 45 | Ethnicity category as provided in the source survey. |

## Notes
- I exported `sample_data.csv` directly from the Excel workbook and did not add any made-up rows.
- Several fields include `Other (Please Specify)` free-text answers, so I would clean those categories more if this were going into a production report.
- The PBIX model references a transformed field named `Average Salary`, but that field is not a raw column in the Excel workbook.

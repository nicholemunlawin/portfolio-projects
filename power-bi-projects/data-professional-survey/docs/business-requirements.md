# Business Requirements

## Project
Data Professional Survey Dashboard

## Why I Built This
I built this dashboard to practice turning raw survey data into a clean Power BI report. The main goal was to make the dataset easier to explore and to highlight useful patterns about people working in or trying to enter the data field.

## What I Wanted To Answer
- What data roles show up the most in the survey?
- How many people switched careers into data?
- Which programming languages do respondents prefer?
- Which countries are most represented?
- How do salary bands compare across roles?
- How satisfied are respondents with salary, work-life balance, coworkers, management, upward mobility, and learning opportunities?
- What matters most to respondents when looking for a new job?

## Intended Users
This project is mainly for portfolio review, but the dashboard could also be useful for:
- Recruiters looking at data talent trends
- Career coaches helping people move into data roles
- Students or career shifters researching the data field
- Analysts reviewing survey-based dashboard design

## Dashboard Pages And Visuals
The Power BI file has one report page named `Data Professional Survey Breakdown`.

I included visuals for:
- Survey summary cards
- Average salary by role
- Favorite programming language by role
- Respondent country distribution
- Satisfaction score gauges
- Gender category and average salary

## Data Scope
- Source file: `data/Data Professional Survey.xlsx`
- Sheet: `Data Professional Survey`
- Rows: 630
- Columns: 28
- Survey dates in the source data: June 10, 2022 to June 26, 2022

## Data Notes
- `Browser`, `OS`, `City`, `Country`, and `Referrer` are blank in the source file.
- `Q12 - Highest Level of Education` has 52 missing values.
- A few satisfaction score fields have missing responses.

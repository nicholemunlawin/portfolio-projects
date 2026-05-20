# Data Dictionary

## Workbook Sheets

| Sheet | Range | Purpose |
|---|---:|---|
| `Dashboard` | `A1:O21` | Main HR dashboard with KPI summaries and visual elements. |
| `Analysis` | `A1:D10` | Business questions, insights, implications, and suggested actions. |
| `Employee_Data` | `A1:Z701` | Employee-level source dataset. |
| `Metrics` | `A1:G25` | Calculated metrics used by the dashboard. |
| `Lookup_Lists` | `A1:A59` | Lookup values used for controlled categories. |

## Employee_Data Fields

| Field | Description |
|---|---|
| `Employee_ID` | Unique employee identifier. |
| `Hire_Date` | Employee hire date stored as an Excel date serial. |
| `Termination_Date` | Termination date when applicable. |
| `Active_Status` | Employee status, such as active or terminated. |
| `Attrition_Flag` | Numeric attrition indicator. |
| `Department` | Employee department. |
| `Job_Level` | Role level or seniority band. |
| `Job_Title` | Employee job title. |
| `Location` | Employee location. |
| `Gender` | Employee gender category. |
| `Age` | Employee age. |
| `Education_Level` | Highest education level category. |
| `Recruitment_Source` | Source or channel through which the employee was recruited. |
| `Employment_Type` | Employment arrangement category. |
| `Annual_Salary` | Annual salary amount. |
| `Monthly_Salary` | Monthly salary amount. |
| `Tenure_Months` | Employee tenure in months. |
| `Performance_Rating` | Performance rating value. |
| `Engagement_Score` | Engagement score value. |
| `Training_Hours` | Training hours completed. |
| `Overtime_Hours_Monthly` | Monthly overtime hours. |
| `Absence_Days` | Number of absence days. |
| `Promotion_Last_2Yrs` | Indicator for whether the employee was promoted in the last two years. |
| `Manager_Rating` | Manager rating value. |
| `Remote_Work_Days` | Number of remote work days. |
| `Commute_Distance_KM` | Commute distance in kilometers. |

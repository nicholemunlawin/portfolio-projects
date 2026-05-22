# DAX Measures

These are the DAX patterns I would use for this dashboard if I rebuild or continue improving the model. The current PBIX mostly uses Power BI visual aggregations, but writing the calculations as measures makes the report easier to maintain.

## Respondent Count
```DAX
Respondent Count =
COUNTROWS('Data Professional Survey')
```

## Career Switchers
```DAX
Career Switchers =
CALCULATE(
    [Respondent Count],
    'Data Professional Survey'[Q2 - Did you switch careers into Data?] = "Yes"
)
```

## Average Age
```DAX
Average Age =
AVERAGE('Data Professional Survey'[Q10 - Current Age])
```

## Average Salary
```DAX
Average Salary =
AVERAGE('Data Professional Survey'[Average Salary])
```

## Average Salary Satisfaction
```DAX
Average Salary Satisfaction =
AVERAGE('Data Professional Survey'[Q6 - How Happy are you in your Current Position with the following? (Salary)])
```

## Average Work Life Balance Satisfaction
```DAX
Average Work Life Balance Satisfaction =
AVERAGE('Data Professional Survey'[Q6 - How Happy are you in your Current Position with the following? (Work/Life Balance)])
```

## Notes
I kept these measures focused on the visuals already used in the dashboard: respondent counts, career switching, average age, average salary, and satisfaction scores.

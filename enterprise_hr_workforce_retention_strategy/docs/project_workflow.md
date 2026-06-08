# Project Workflow

## 1. Why

The business objective is to help HR leaders understand workforce retention, attrition behavior, employee lifecycle patterns, and data quality risks.

## 2. How

The project uses Python for data cleaning and Power BI for visualization.

Workflow:

1. Import raw HR data
2. Standardize column names
3. Clean text fields
4. Convert date and numeric columns
5. Treat missing values
6. Remove duplicate records
7. Create attrition and retention flags
8. Create tenure and age bands
9. Add data quality flags
10. Export cleaned dataset
11. Build Power BI dashboard

## 3. Result

The final result is an HR analytics dashboard supported by a clean dataset and reusable Python pipeline.

## 4. Proof

Proof is stored in:

- `src/hr_data_cleaning.py`
- `powerbi/Enterprise_HR_Workforce_Retention_Strategy.pbix`
- `assets/screenshots/`

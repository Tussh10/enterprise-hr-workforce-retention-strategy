# Data Dictionary

## Cleaned Dataset: HR_Clean_Dataset.csv

| Column Name | Description |
|---|---|
| snapshot_date | HR snapshot date for the record |
| snapshot_year | Year extracted from snapshot date |
| snapshot_month | Month number extracted from snapshot date |
| snapshot_month_name | Month name extracted from snapshot date |
| employee_id | Unique employee identifier |
| gender | Employee gender category |
| age | Employee age |
| age_band | Grouped employee age range |
| age_group_id | Original age group identifier |
| ethnic_group_id | Employee ethnic group identifier |
| business_unit_id | Business unit identifier |
| employment_type_code | Employment type code |
| pay_type_id | Pay type identifier |
| hire_date | Employee hire date |
| hire_year | Year extracted from hire date |
| hire_month | Month extracted from hire date |
| tenure_days | Employee tenure in days |
| tenure_months | Employee tenure in months |
| tenure_years | Employee tenure in years |
| tenure_band | Grouped tenure range |
| is_new_hire | New hire indicator |
| termination_date | Employee termination date, if applicable |
| termination_reason_code | Termination reason code |
| employee_status | Active or terminated employee status |
| attrition_flag | 1 if terminated, otherwise 0 |
| retention_flag | 1 if retained, otherwise 0 |
| hire_after_snapshot_month_flag | Flags records where hire date is after the snapshot month |
| termination_before_hire_flag | Flags records where termination date is before hire date |
| termination_after_snapshot_month_flag | Flags records where termination date is after the snapshot month |
| data_quality_issue_flag | Combined flag for any detected date-quality issue |

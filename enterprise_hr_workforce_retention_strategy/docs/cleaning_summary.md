# Cleaning Summary

## Project Name

**Enterprise HR Workforce & Employee Retention Strategy**

## Purpose of Cleaning

The purpose of this cleaning process is to convert the raw HR workforce dataset into a clean, consistent, reliable, and analysis-ready dataset for employee retention analysis, attrition tracking, workforce monitoring, and Power BI dashboard reporting.

The cleaning workflow prepares the data for downstream analysis by resolving formatting issues, standardizing column names, correcting data types, handling missing values, removing duplicate records, creating business-ready HR metrics, and adding data quality validation flags.

---

## Source Dataset

The raw dataset contains enterprise HR workforce records with employee-level information such as employee ID, gender, age, business unit, hire date, termination date, pay type, employment type, tenure, and termination reason.

The raw dataset is treated as the source layer and should be stored locally in:

```text
data/raw/
```

> Note: Raw HR data should not be uploaded to a public GitHub repository unless it is synthetic, anonymized, or approved for public sharing.

---

## Cleaned Dataset Outputs

The cleaning process produces two cleaned dataset formats:

```text
data/processed/HR_Clean_Dataset.csv
```

### CSV Output

The CSV version is suitable for:

- Python analysis
- Power BI import
- Reproducible analytics workflows
- Lightweight data sharing

### Excel Output

The Excel version is suitable for:

- Manual review
- Business stakeholder validation
- Portfolio presentation
- Quick inspection without running Python

---

## Cleaning Workflow Summary

The cleaning process follows a structured data analyst project lifecycle before visualization.

### 1. Data Import

The raw HR dataset is imported using Python and pandas.

Key actions:

- Imported the raw CSV file.
- Defined raw columns as string where needed.
- Used controlled missing value recognition.
- Disabled low-memory type guessing to avoid inconsistent column inference.

This step ensures the raw data is loaded safely before transformation.

---

### 2. Column Standardization

Original column names were renamed into clean, readable, analytics-friendly names.

| Raw Column | Cleaned Column |
|---|---|
| `date` | `snapshot_date` |
| `EmplID` | `employee_id` |
| `Gender` | `gender` |
| `TermDate` | `termination_date` |
| `HireDate` | `hire_date` |
| `BU` | `business_unit_id` |
| `PayTypeID` | `pay_type_id` |
| `TermReason` | `termination_reason_code` |
| `TenureDays` | `tenure_days` |
| `TenureMonths` | `tenure_months` |

Additional standardization included:

- Removing leading and trailing spaces from column names.
- Converting column names to lowercase.
- Replacing spaces with underscores.

This improves readability, consistency, and compatibility with Python and Power BI.

---

### 3. Text Data Cleaning

Text-based fields were cleaned to reduce inconsistencies caused by casing or whitespace.

Fields cleaned:

- `gender`
- `employment_type_code`
- `pay_type_id`
- `termination_reason_code`

Key actions:

- Converted text values to string format.
- Removed unnecessary spaces.
- Converted values to uppercase.

This prevents duplicate category issues such as `Male`, `male`, and `MALE` being treated as separate values.

---

### 4. Date Conversion

Date columns were converted into proper datetime format.

Date columns converted:

- `snapshot_date`
- `hire_date`
- `termination_date`

Invalid or unreadable dates were converted to missing values using safe parsing.

This enables reliable time-based calculations such as tenure analysis, monthly workforce snapshots, hire trends, and termination tracking.

---

### 5. Numeric Conversion

Numeric fields were converted from raw string format into numeric format.

Numeric columns converted:

- `employee_id`
- `age`
- `ethnic_group_id`
- `business_unit_id`
- `age_group_id`
- `tenure_days`
- `tenure_months`
- `is_new_hire`

Invalid numeric values were safely converted to missing values for later handling or validation.

---

### 6. Missing Value Treatment

Missing values were handled based on business logic.

Key rules:

- Missing `is_new_hire` values were filled with `0`.
- Missing termination reason values were classified based on employee status.
- Active employees were assigned `NOT_TERMINATED`.
- Terminated employees with missing termination reasons were assigned `UNKNOWN`.
- Records missing critical identifiers or dates were removed.

Critical fields required:

- `employee_id`
- `snapshot_date`
- `hire_date`

This ensures core HR records remain usable and logically complete.

---

### 7. Duplicate Handling

Duplicate records were removed to prevent inflated employee counts and inaccurate attrition calculations.

Actions performed:

- Removed exact duplicate rows.
- Created an `attrition_flag` before advanced duplicate handling.
- Sorted records by employee, snapshot date, attrition status, and termination date.
- Kept the most relevant record for each employee and snapshot period.

Duplicate handling is important because duplicate employee-month records can distort:

- Headcount
- Attrition rate
- Retention rate
- Termination count
- Workforce distribution

---

### 8. Business Rule Cleaning

Business rules were applied to ensure the dataset aligns with realistic HR assumptions.

Rules applied:

- Employee age must be between 16 and 100.
- Negative tenure days were clipped to 0.
- Negative tenure months were clipped to 0.
- Employee status was created using termination information.
- Retention and attrition flags were created.

Created fields:

| Field | Description |
|---|---|
| `employee_status` | Identifies employees as `ACTIVE` or `TERMINATED` |
| `attrition_flag` | 1 if terminated, 0 otherwise |
| `retention_flag` | 1 if active, 0 if terminated |

These fields support Power BI KPI calculations and HR dashboard metrics.

---

### 9. Feature Preparation

New analytical features were created to make the dataset dashboard-ready.

Date features:

- `snapshot_year`
- `snapshot_month`
- `snapshot_month_name`
- `hire_year`
- `hire_month`

Tenure features:

- `tenure_years`
- `tenure_band`

Age features:

- `age_band`

Tenure bands created:

| Tenure Band | Meaning |
|---|---|
| `0-6 MONTHS` | New or early-stage employees |
| `7-12 MONTHS` | First-year employees |
| `1-2 YEARS` | Early-tenure employees |
| `2-5 YEARS` | Established employees |
| `5-10 YEARS` | Experienced employees |
| `10+ YEARS` | Long-tenure employees |

Age bands created:

| Age Band |
|---|
| `16-24` |
| `25-34` |
| `35-44` |
| `45-54` |
| `55-64` |
| `65+` |

These features make the dataset easier to analyze in Power BI using slicers, filters, and grouped visuals.

---

### 10. Data Quality Flags

Data quality validation flags were created to identify records that may require review.

Created flags:

| Flag | Purpose |
|---|---|
| `hire_after_snapshot_month_flag` | Identifies records where hire date is after the snapshot month |
| `termination_before_hire_flag` | Identifies records where termination date is before hire date |
| `termination_after_snapshot_month_flag` | Identifies records where termination date is after the snapshot month |
| `data_quality_issue_flag` | Combined flag showing whether any date quality issue exists |

These flags do not automatically delete records. They allow the analyst or business user to review potential data issues before making decisions.

This is important because incorrect hire or termination dates can affect:

- Active employee count
- Terminated employee count
- Attrition rate
- Retention rate
- Tenure calculations
- Workforce trend analysis

---

### 11. Final Type Optimization

Columns were optimized into appropriate data types to improve memory usage, performance, and reporting consistency.

Actions performed:

- Integer columns were converted to nullable integer format where needed.
- Category columns were converted to category type.
- Date columns were kept as datetime fields.
- Flags were stored efficiently as integer indicators.

This helps the cleaned dataset perform better when loaded into Power BI or reused in Python.

---

### 12. Final Column Ordering

The final dataset columns were arranged logically for readability and business use.

Column groups were organized around:

1. Snapshot information
2. Employee demographic details
3. Employment and business unit details
4. Hire and tenure information
5. Termination and employee status fields
6. Retention and attrition flags
7. Data quality validation flags

This improves usability for both technical and non-technical users.

---

### 13. Cleaned Dataset Export and Import

The final cleaned dataset was exported and re-imported to confirm that the output file can be reused successfully.

Primary cleaned file:

```text
HR_Clean_Dataset.csv
```

Optional business-friendly file:

```text
HR_Clean_Dataset.xlsx
```

This step supports reproducibility and confirms the cleaned dataset is ready for Power BI.

---

## Final Cleaned Dataset Fields

The cleaned dataset includes the following columns:

```text
snapshot_date
snapshot_year
snapshot_month
snapshot_month_name
employee_id
gender
age
age_band
age_group_id
ethnic_group_id
business_unit_id
employment_type_code
pay_type_id
hire_date
hire_year
hire_month
tenure_days
tenure_months
tenure_years
tenure_band
is_new_hire
termination_date
termination_reason_code
employee_status
attrition_flag
retention_flag
hire_after_snapshot_month_flag
termination_before_hire_flag
termination_after_snapshot_month_flag
data_quality_issue_flag
```

---

## Key Business Metrics Enabled

The cleaned dataset enables the following HR analytics metrics:

- Total workforce count
- Active employee count
- Terminated employee count
- Attrition rate
- Retention rate
- New hire count
- Tenure distribution
- Workforce distribution by business unit
- Attrition by gender
- Attrition by age band
- Attrition by tenure band
- Attrition by employment type
- Data quality issue count

---

## Power BI Usage

The cleaned dataset is used as the prepared input for the Power BI dashboard.

Power BI file location:

```text
powerbi/Enterprise_HR_Workforce_Retention_Strategy.pbix
```

The dashboard is expected to include:

- Executive HR KPI overview
- Workforce distribution analysis
- Attrition and retention analysis
- Tenure-based employee insights
- Demographic workforce breakdown
- Data quality monitoring

---

## Reproducibility

To reproduce the cleaning process:

1. Place the raw HR dataset in:

```text
data/raw/
```

2. Run the Python cleaning script:

```bash
python src/hr_data_cleaning.py
```

3. Save the generated cleaned datasets in:

```text
data/processed/
```

4. Load the cleaned dataset into Power BI.

---

## Data Privacy Note

HR data can contain sensitive employee information. Before uploading datasets to a public GitHub repository, confirm that the data is:

- Synthetic
- Anonymized
- Publicly shareable
- Approved for portfolio use

If the data contains real employee information, do not publish the raw dataset publicly.

---

## Summary

This cleaning process converts raw HR workforce data into a structured, reliable, and analysis-ready dataset. The final cleaned dataset supports workforce monitoring, attrition analysis, employee retention strategy, and executive HR reporting through Power BI.

The cleaning workflow demonstrates a complete data preparation process before visualization, including import, standardization, cleaning, validation, feature preparation, quality control, export, and documentation.

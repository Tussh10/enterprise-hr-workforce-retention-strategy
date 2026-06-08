# Project: Enterprise HR Workforce & Employee Retention Strategy
# Phase: Data import, cleaning, preparation, validation, and cleaned dataset import
# Note: Visualization is intentionally not included. As the Visualization phase will be handled separately in a Power BI file, the focus here is solely on data cleaning and preparation to ensure a clean and structured dataset for analysis and visualization in Power BI.

import pandas as pd
import numpy as np




# 1. Raw Dataset Import
# ===========================================================================================================


RAW_DATA_PATH = "/mnt/data/HR_Raw_1800000rows_15cols.csv"
CLEAN_DATA_PATH = "HR_Clean_Dataset.csv"

raw_dtype = {
    "date": "string",
    "EmplID": "string",
    "Gender": "string",
    "Age": "string",
    "EthnicGroup": "string",
    "FP": "string",
    "TermDate": "string",
    "isNewHire": "string",
    "BU": "string",
    "HireDate": "string",
    "PayTypeID": "string",
    "TermReason": "string",
    "AgeGroupID": "string",
    "TenureDays": "string",
    "TenureMonths": "string"
}

HR_Clean_Dataset = pd.read_csv(
    RAW_DATA_PATH,
    dtype=raw_dtype,
    na_values=["", " ", "NA", "N/A", "NULL", "null", "None", "none", "nan"],
    keep_default_na=True,
    low_memory=False
)




# 2. Column Standardization
# ===========================================================================================================


HR_Clean_Dataset = HR_Clean_Dataset.rename(columns={
    "date": "snapshot_date",
    "EmplID": "employee_id",
    "Gender": "gender",
    "Age": "age",
    "EthnicGroup": "ethnic_group_id",
    "FP": "employment_type_code",
    "TermDate": "termination_date",
    "isNewHire": "is_new_hire",
    "BU": "business_unit_id",
    "HireDate": "hire_date",
    "PayTypeID": "pay_type_id",
    "TermReason": "termination_reason_code",
    "AgeGroupID": "age_group_id",
    "TenureDays": "tenure_days",
    "TenureMonths": "tenure_months"
})

HR_Clean_Dataset.columns = (
    HR_Clean_Dataset.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_", regex=False)
)







# 3. Text Data Cleaning
# ===========================================================================================================


text_columns = [
    "gender",
    "employment_type_code",
    "pay_type_id",
    "termination_reason_code"
]

for col in text_columns:
    HR_Clean_Dataset[col] = (
        HR_Clean_Dataset[col]
        .astype("string")
        .str.strip()
        .str.upper()
    )







# 4. Data Type Conversion
# ===========================================================================================================


date_columns = [
    "snapshot_date",
    "hire_date",
    "termination_date"
]

for col in date_columns:
    HR_Clean_Dataset[col] = pd.to_datetime(
        HR_Clean_Dataset[col],
        errors="coerce"
    )

numeric_columns = [
    "employee_id",
    "age",
    "ethnic_group_id",
    "business_unit_id",
    "age_group_id",
    "tenure_days",
    "tenure_months",
    "is_new_hire"
]

for col in numeric_columns:
    HR_Clean_Dataset[col] = pd.to_numeric(
        HR_Clean_Dataset[col],
        errors="coerce"
    )






# 5. Missing Value Treatment
# ===========================================================================================================


HR_Clean_Dataset["is_new_hire"] = (
    HR_Clean_Dataset["is_new_hire"]
    .fillna(0)
    .astype("int8")
)

HR_Clean_Dataset["termination_reason_code"] = np.where(
    HR_Clean_Dataset["termination_date"].notna(),
    HR_Clean_Dataset["termination_reason_code"].fillna("UNKNOWN"),
    "NOT_TERMINATED"
)

HR_Clean_Dataset = HR_Clean_Dataset.dropna(
    subset=[
        "employee_id",
        "snapshot_date",
        "hire_date"
    ]
)







# 6. Duplicate Handling
# ===========================================================================================================


HR_Clean_Dataset = HR_Clean_Dataset.drop_duplicates()

HR_Clean_Dataset["attrition_flag"] = (
    HR_Clean_Dataset["termination_date"]
    .notna()
    .astype("int8")
)

HR_Clean_Dataset = (
    HR_Clean_Dataset
    .sort_values(
        by=[
            "employee_id",
            "snapshot_date",
            "attrition_flag",
            "termination_date"
        ],
        ascending=[True, True, True, True],
        na_position="first"
    )
    .drop_duplicates(
        subset=[
            "employee_id",
            "snapshot_date"
        ],
        keep="last"
    )
    .reset_index(drop=True)
)







# ===========================================================================================================
# 7. Business Rule Cleaning
# ===========================================================================================================


HR_Clean_Dataset["age"] = HR_Clean_Dataset["age"].where(
    HR_Clean_Dataset["age"].between(16, 100),
    np.nan
)

HR_Clean_Dataset["tenure_days"] = HR_Clean_Dataset["tenure_days"].clip(lower=0)
HR_Clean_Dataset["tenure_months"] = HR_Clean_Dataset["tenure_months"].clip(lower=0)

HR_Clean_Dataset["employee_status"] = np.where(
    HR_Clean_Dataset["attrition_flag"] == 1,
    "TERMINATED",
    "ACTIVE"
)

HR_Clean_Dataset["retention_flag"] = np.where(
    HR_Clean_Dataset["attrition_flag"] == 1,
    0,
    1
).astype("int8")






# ===========================================================================================================
# 8. Feature Preparation
# ===========================================================================================================


HR_Clean_Dataset["snapshot_year"] = HR_Clean_Dataset["snapshot_date"].dt.year
HR_Clean_Dataset["snapshot_month"] = HR_Clean_Dataset["snapshot_date"].dt.month
HR_Clean_Dataset["snapshot_month_name"] = HR_Clean_Dataset["snapshot_date"].dt.month_name()

HR_Clean_Dataset["hire_year"] = HR_Clean_Dataset["hire_date"].dt.year
HR_Clean_Dataset["hire_month"] = HR_Clean_Dataset["hire_date"].dt.month

HR_Clean_Dataset["tenure_years"] = (
    HR_Clean_Dataset["tenure_days"] / 365.25
).round(2)

HR_Clean_Dataset["tenure_band"] = pd.cut(
    HR_Clean_Dataset["tenure_months"],
    bins=[-1, 6, 12, 24, 60, 120, np.inf],
    labels=[
        "0-6 MONTHS",
        "7-12 MONTHS",
        "1-2 YEARS",
        "2-5 YEARS",
        "5-10 YEARS",
        "10+ YEARS"
    ]
)

HR_Clean_Dataset["age_band"] = pd.cut(
    HR_Clean_Dataset["age"],
    bins=[15, 24, 34, 44, 54, 64, 100],
    labels=[
        "16-24",
        "25-34",
        "35-44",
        "45-54",
        "55-64",
        "65+"
    ]
)






# ===========================================================================================================
# 9. Data Quality Flags
# ===========================================================================================================


snapshot_month_end = HR_Clean_Dataset["snapshot_date"] + pd.offsets.MonthEnd(0)

HR_Clean_Dataset["hire_after_snapshot_month_flag"] = (
    HR_Clean_Dataset["hire_date"] > snapshot_month_end
).astype("int8")

HR_Clean_Dataset["termination_before_hire_flag"] = (
    HR_Clean_Dataset["termination_date"].notna()
    & (HR_Clean_Dataset["termination_date"] < HR_Clean_Dataset["hire_date"])
).astype("int8")

HR_Clean_Dataset["termination_after_snapshot_month_flag"] = (
    HR_Clean_Dataset["termination_date"].notna()
    & (HR_Clean_Dataset["termination_date"] > snapshot_month_end)
).astype("int8")

HR_Clean_Dataset["data_quality_issue_flag"] = (
    (
        HR_Clean_Dataset["hire_after_snapshot_month_flag"]
        + HR_Clean_Dataset["termination_before_hire_flag"]
        + HR_Clean_Dataset["termination_after_snapshot_month_flag"]
    ) > 0
).astype("int8")






# ===========================================================================================================
# 10. Final Type Optimization
# ===========================================================================================================


integer_columns = [
    "employee_id",
    "age",
    "ethnic_group_id",
    "business_unit_id",
    "age_group_id",
    "tenure_months",
    "snapshot_year",
    "snapshot_month",
    "hire_year",
    "hire_month"
]

for col in integer_columns:
    HR_Clean_Dataset[col] = HR_Clean_Dataset[col].astype("Int64")

category_columns = [
    "gender",
    "employment_type_code",
    "pay_type_id",
    "termination_reason_code",
    "employee_status",
    "tenure_band",
    "age_band",
    "snapshot_month_name"
]

for col in category_columns:
    HR_Clean_Dataset[col] = HR_Clean_Dataset[col].astype("category")








# ===========================================================================================================
# 11. Final Column Ordering
# ===========================================================================================================


final_columns = [
    "snapshot_date",
    "snapshot_year",
    "snapshot_month",
    "snapshot_month_name",
    "employee_id",
    "gender",
    "age",
    "age_band",
    "age_group_id",
    "ethnic_group_id",
    "business_unit_id",
    "employment_type_code",
    "pay_type_id",
    "hire_date",
    "hire_year",
    "hire_month",
    "tenure_days",
    "tenure_months",
    "tenure_years",
    "tenure_band",
    "is_new_hire",
    "termination_date",
    "termination_reason_code",
    "employee_status",
    "attrition_flag",
    "retention_flag",
    "hire_after_snapshot_month_flag",
    "termination_before_hire_flag",
    "termination_after_snapshot_month_flag",
    "data_quality_issue_flag"
]

HR_Clean_Dataset = HR_Clean_Dataset[final_columns]








# ===========================================================================================================
# 12. Cleaned Dataset Export
# ===========================================================================================================


HR_Clean_Dataset.to_csv(
    CLEAN_DATA_PATH,
    index=False
)





# ===========================================================================================================
# 13. Cleaned Dataset Import
# ===========================================================================================================


HR_Clean_Dataset = pd.read_csv(
    CLEAN_DATA_PATH,
    parse_dates=[
        "snapshot_date",
        "hire_date",
        "termination_date"
    ],
    low_memory=False
)

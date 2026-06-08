# Enterprise HR Workforce & Employee Retention Strategy

## Project Overview

This project analyzes enterprise HR workforce data to support employee retention strategy, workforce monitoring, attrition tracking, and HR decision-making. The Python script handles data importing, cleaning, preparation, validation, and cleaned dataset export. The final business dashboard is built in Power BI.

---

## 1. Why

Employee retention is a critical business problem because high attrition can increase hiring cost, reduce productivity, disrupt team performance, and impact long-term workforce planning.

This project was created to answer key HR business questions such as:

- What is the current workforce size?
- How many employees are active versus terminated?
- Which employee groups show higher attrition?
- How does tenure relate to retention?
- Are there workforce trends by business unit, age group, gender, or employment type?
- Are there data quality issues that may affect HR reporting accuracy?

The goal is to transform raw HR data into a clean, analysis-ready dataset and use Power BI to communicate workforce and retention insights clearly.

---

## 2. How

The project follows a standard data analyst project lifecycle up to dashboarding:

### Step 1: Data Import

The raw HR dataset is imported using Python and pandas. Data types are controlled during import to prevent incorrect automatic type inference.

### Step 2: Data Cleaning

The cleaning script performs:

- Column renaming and standardization
- Text formatting and whitespace removal
- Date conversion
- Numeric conversion
- Missing value treatment
- Duplicate record handling
- Business rule validation
- Employee attrition and retention flag creation
- Tenure and age band creation
- Data quality issue flagging

### Step 3: Cleaned Dataset Export

The cleaned dataset is exported as:

```text
HR_Clean_Dataset.csv
```

This file becomes the prepared input for Power BI.

### Step 4: Power BI Dashboarding

Power BI is used for visualization, dashboard creation, KPI reporting, and executive-level storytelling.

---

## 3. Result

The final output of this project includes:

- A cleaned HR dataset ready for analysis
- A reusable Python cleaning script
- A Power BI dashboard file
- A documented GitHub repository structure
- Data quality flags to support trustworthy reporting

Expected dashboard outcomes include:

- Active employee count
- Terminated employee count
- Attrition rate
- Retention rate
- Workforce distribution by business unit
- Attrition analysis by age band, gender, tenure band, and employment type
- Data quality issue identification

---

## 4. Proof

Proof of work is included through the following project assets:

### Python Cleaning Script

Located at:

```text
src/hr_data_cleaning.py
```

This script proves the data preparation process, including cleaning, transformation, feature preparation, and validation.

### Power BI Report

Located at:

```text
powerbi/Enterprise_HR_Workforce_Retention_Strategy.pbix
```

This file proves the dashboarding and visualization work completed in Power BI.

### Screenshots

Dashboard screenshots should be added here before publishing the repository:

```text
assets/screenshots/
```

Recommended screenshots:

- Dashboard overview page
- Attrition analysis page
- Retention analysis page
- Workforce demographics page
- Data quality or validation page

---

## Repository Structure

```text
enterprise_hr_workforce_retention_strategy/
│
├── README.md
├── requirements.txt
├── .gitignore
│
├── src/
│   └── hr_data_cleaning.py
│
├── data/
│   ├── raw/
│   │   └── .gitkeep
│   └── processed/
│       └── HR_Clean_Dataset.csv
│       
├── powerbi/
│   └── Enterprise_HR_Workforce_Retention_Strategy.pbix
│
├── docs/
│   ├── data_dictionary.md
│   ├── project_workflow.md
│   └── cleaning_summary.md
│
└── assets/
    └── screenshots/
        ├── Chart 1.png
        ├── Chart 2.png
        ├── Chart 3.png
        ├── Chart 4.png
        └── .gitkeep
```



## Tools Used

- Python
- pandas
- NumPy
- Power BI
- GitHub

---

## How to Run

1. Place the raw HR CSV file inside:

```text
data/raw/
```

2. Update the file path in `src/hr_data_cleaning.py` if required.

3. Run the Python script:

```bash
python src/hr_data_cleaning.py
```

4. Use the generated cleaned dataset in Power BI.

---

## Notes

The raw HR dataset is not included in this GitHub package by default because HR data may contain sensitive employee information. Only folder placeholders are provided for raw and processed data.

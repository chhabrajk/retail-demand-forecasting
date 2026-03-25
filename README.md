# 🔗 Automated ETL Pipeline

> **Repo name:** `automated-etl-pipeline`
> **Description:** Production-style ETL pipeline — Extract, Clean, Transform, Load to SQLite, and auto-generate a PDF analytics report with charts. Zero manual steps.

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat-square&logo=pandas&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=flat-square&logo=sqlite&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-11557C?style=flat-square)

> 🚀 **[Live Demo →](https://chhabrajk.github.io/automated-etl-pipeline/demo.html)**
> *(Run the script locally → upload `output/etl_report_charts.png` → enable GitHub Pages)*

---

## 🎯 Business Problem

Finance and ops teams waste hours every week doing the same thing:
download a file → clean it in Excel → copy-paste into a report → send it out.

**This ETL pipeline automates the entire workflow** — from raw messy data
to a clean SQLite database and a PDF report — in a single command.

---

## 📊 What It Does

### Stage 1 — Extract
- Simulates ingestion from a raw data source (CSV / API / database)
- Injects realistic dirty data: duplicates, negative values, nulls

### Stage 2 — Transform & Clean
- Removes duplicate records
- Fixes and imputes invalid/missing values
- Engineers derived columns: `revenue`, `order_month`, `order_quarter`, `age_group`, `is_high_value`
- Logs every transformation with timestamp

### Stage 3 — Load
- Writes clean data to **SQLite** (`analytics.db`)
- Creates aggregated summary tables: `monthly_summary`, `category_summary`

### Stage 4 — Report
- Generates a **6-panel Matplotlib chart** (`output/etl_report_charts.png`)
- Builds a formatted **PDF report** (`output/etl_analytics_report.pdf`) with KPI table + charts

---

## 🖼️ Output Files

> 📸 **Add screenshots here after running locally.**
> Upload files from the `output/` folder into a `/screenshots` folder in this repo.

![ETL Charts](screenshots/etl_report_charts.png)

| File | Description |
|------|-------------|
| `analytics.db` | SQLite database with 3 tables |
| `output/etl_report_charts.png` | 6-panel analytics chart |
| `output/etl_analytics_report.pdf` | Full PDF report with KPIs |

> 🌐 **[View Sample Report →](https://chhabrajk.github.io/automated-etl-pipeline/demo.html)**

---

## 🚀 Quick Start

```bash
# 1. Clone the repo
git clone https://github.com/chhabrajk/automated-etl-pipeline.git
cd automated-etl-pipeline

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the pipeline
python main_script.py

# Outputs → output/ folder + analytics.db
```

---

## 📁 Repo Structure

```
automated-etl-pipeline/
├── main_script.py       ← Full ETL pipeline
├── requirements.txt
├── output/              ← Auto-created on run
│   ├── etl_report_charts.png
│   └── etl_analytics_report.pdf
├── screenshots/         ← Add output screenshots here
└── README.md
```

---

## 📦 Requirements

```txt
pandas==2.2.2
numpy==1.26.4
matplotlib==3.8.4
reportlab==4.2.0
```

---

## 🧰 Data Quality Issues Handled

| Issue | How Handled |
|-------|-------------|
| Duplicate rows | Removed via `drop_duplicates()` |
| Negative customer ages | Set to NaN, then median-imputed |
| Missing values | Median imputation with logging |
| Inconsistent types | Cast during transformation stage |

---

## 💡 Sample Console Output

```
08:12:01 [INFO] EXTRACT — Loading raw data...
08:12:01 [INFO]    Raw rows extracted: 3,060
08:12:01 [INFO] TRANSFORM — Cleaning & enriching data...
08:12:01 [INFO]    Duplicates removed  : 60
08:12:01 [INFO]    Invalid ages fixed  : 90
08:12:01 [INFO]    Missing ages imputed: 60
08:12:01 [INFO]    Clean rows          : 3,000
08:12:01 [INFO] LOAD — Writing to SQLite: analytics.db
08:12:02 [INFO] REPORT — Generating charts & PDF report...

PIPELINE COMPLETE ✅
Total Revenue       : $2,341,882
Total Orders        : 3,000
Avg Order Value     : $780.63
Top Category        : Electronics
Top Region          : West
⏱️  Completed in 3s
```

---

## 👤 Author

**JK Chhabra** — Senior Data Analytics Consultant
- 🌐 [GitHub](https://github.com/chhabrajk)
- 💼 [Upwork](#)
- 📧 jsinfo618@gmail.com

---

*Part of the [Analytics Portfolio](https://github.com/chhabrajk) — 6 end-to-end data projects.*
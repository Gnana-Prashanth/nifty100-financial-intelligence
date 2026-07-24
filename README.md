# 📈 Nifty100 Financial Intelligence Dashboard

> A comprehensive Financial Intelligence Platform built using **Python, SQLite, Pandas, Plotly, and Streamlit** to analyze the financial performance of all **92 Nifty 100 companies**.

![Python](https://img.shields.io/badge/Python-3.x-blue)
![SQLite](https://img.shields.io/badge/SQLite-Database-green)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-orange)
![Plotly](https://img.shields.io/badge/Plotly-Visualization-blueviolet)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-red)

---

# 📌 Project Overview

The **Nifty100 Financial Intelligence Dashboard** is an end-to-end financial analytics platform developed to analyze listed Indian companies using publicly available financial statements.

The project starts with raw Excel datasets, validates and cleans the data through an ETL pipeline, stores the processed information in SQLite, computes financial KPIs, generates screening and peer comparison reports, and finally presents the results through an interactive Streamlit dashboard.

The application supports financial analysis across **92 Nifty 100 companies** covering multiple sectors including Information Technology, Banking & Financial Services, FMCG, Energy, Healthcare, Automobile, Telecom, Cement, Metals, Chemicals, and Infrastructure.

---

# 🎯 Project Objectives

- Build a complete financial analytics pipeline from raw Excel files.
- Create a validated SQLite database for financial analysis.
- Compute profitability, leverage, growth, efficiency, and cash-flow KPIs.
- Develop configurable stock screeners with multiple investment presets.
- Perform peer-group percentile analysis and benchmarking.
- Generate professional Excel reports and radar charts.
- Build an interactive Streamlit dashboard for exploring financial insights.
- Implement valuation analytics using market multiples and Free Cash Flow Yield.

---

# ✨ Key Features

## 📂 Data Foundation

- ETL pipeline for loading financial datasets
- Excel data validation and normalization
- SQLite database integration
- Automated data quality checks
- Manual data quality review
- Validation reports and audit logs

---

## 📊 Financial Analytics

The project computes **50+ financial KPIs**, including:

### Profitability

- Net Profit Margin (NPM)
- Operating Profit Margin (OPM)
- Return on Equity (ROE)
- Return on Capital Employed (ROCE)
- Return on Assets (ROA)

### Leverage & Efficiency

- Debt to Equity Ratio
- Interest Coverage Ratio
- Asset Turnover Ratio
- Net Debt

### Growth Metrics

- Revenue CAGR
- PAT CAGR
- EPS CAGR

for:

- 3 Years
- 5 Years
- 10 Years

### Cash Flow Metrics

- Free Cash Flow (FCF)
- CFO Quality Score
- CapEx Intensity
- FCF Conversion Ratio

### Quality Metrics

- Composite Quality Score
- Sector-relative ranking

### Capital Allocation

Classification of companies into capital allocation patterns based on operating, investing, and financing cash flows.

### Valuation

- P/E Ratio
- P/B Ratio
- EV/EBITDA
- FCF Yield
- Sector Median P/E
- Valuation Flags (Fair / Discount / Caution)

---

# 🔍 Financial Screening

The application supports configurable stock screening using multiple financial filters.

Built-in screening presets include:

- ✅ Quality Compounder
- ✅ Value Pick
- ✅ Growth Accelerator
- ✅ Dividend Champion
- ✅ Debt-Free Blue Chip
- ✅ Turnaround Watch

Users can also apply custom threshold filters across multiple financial metrics.

---

# 📊 Peer Group Analysis

The platform performs peer-level benchmarking by:

- Computing percentile rankings
- Comparing companies within peer groups
- Generating radar charts
- Exporting peer comparison reports
- Ranking companies across multiple financial metrics

---

# 🖥 Interactive Dashboard

The Streamlit dashboard provides **8 interactive pages**:

1. Home Dashboard
2. Company Profile
3. Financial Screener
4. Peer Comparison
5. Trend Analysis
6. Sector Analysis
7. Capital Allocation
8. Annual Reports

The dashboard supports:

- Company search
- Interactive Plotly charts
- KPI cards
- Financial tables
- CSV downloads
- Valuation analytics
- Trend visualization


# 🏗 Project Architecture

The project follows a modular architecture where each component is responsible for a specific stage of the financial analytics pipeline.

```
                    Raw Excel Files
                           │
                           ▼
                  ETL & Data Validation
                           │
                           ▼
                    SQLite Database
                           │
          ┌────────────────┼────────────────┐
          │                │                │
          ▼                ▼                ▼
   Analytics Engine   Screener Engine   Reporting
          │                │                │
          └────────────────┼────────────────┘
                           ▼
                  Streamlit Dashboard
                           │
                           ▼
                  Interactive Visualizations
```

The architecture separates data ingestion, analytics, reporting, screening, and dashboard modules, making the project modular, maintainable, and scalable.

---

# 📁 Repository Structure

```
NIFTY100_FINANCIAL_INTELLIGENCE/
│
├── config/
│   └── screener_config.yaml
│
├── data/
│   ├── raw/
│   │   ├── analysis.xlsx
│   │   ├── balancesheet.xlsx
│   │   ├── cashflow.xlsx
│   │   ├── companies.xlsx
│   │   ├── documents.xlsx
│   │   ├── profitandloss.xlsx
│   │   └── prosandcons.xlsx
│   │
│   └── supporting/
│       ├── financial_ratios.xlsx
│       ├── market_cap.xlsx
│       ├── peer_groups.xlsx
│       ├── sectors.xlsx
│       └── stock_prices.xlsx
│
├── db/
│   ├── create_db.py
│   ├── check_db.py
│   ├── check_rows.py
│   └── schema.sql
│
├── docs/
│   ├── sprint1_retrospective.md
│   ├── sprint2_retrospective.md
│   ├── sprint3_retrospective.md
│   └── sprint4_retrospective.md
│
├── notebooks/
│   ├── apply_normalization.py
│   ├── inspect_data.py
│   ├── day6_manual_review_queries.py
│   ├── day6_review_companies.py
│   ├── day14_demo.py
│   ├── day14_screener.py
│   ├── exploratory_queries.sql
│   └── manual_review_notes.md
│
├── output/
│   ├── capital_allocation.csv
│   ├── compounder_screener.csv
│   ├── dividend_screener.csv
│   ├── growth_screener.csv
│   ├── turnaround_screener.csv
│   ├── value_screener.csv
│   ├── quality_screener.csv
│   ├── screener.csv
│   ├── screener_output.xlsx
│   ├── peer_comparison.xlsx
│   ├── valuation_summary.xlsx
│   ├── valuation_flags.csv
│   ├── load_audit.csv
│   ├── validation_failures.csv
│   ├── ratio_edge_cases.log
│   └── generate_validation_report.py
│
├── reports/
│   └── radar_charts/
│
├── src/
│   ├── analytics/
│   │   ├── ratios.py
│   │   ├── cagr.py
│   │   ├── cashflow.py
│   │   ├── composite_score.py
|   |   ├── day13_edge_cases.py
│   │   ├── peer.py
│   │   ├── quality_metrics.py
|   |   ├── test_quality_metrics.py
│   │   ├── generate_capital_allocation.py
│   │   ├── populate_financial_ratios.py
│   │   └── valuation.py
│   │
│   ├── api/
│   │   └── routers/
│   │
│   ├── dashboard/
│   │   ├── app.py
│   │   ├── pages/
│   │   │   ├── 01_home.py
│   │   │   ├── 02_profile.py
│   │   │   ├── 03_screener.py
│   │   │   ├── 04_peers.py
│   │   │   ├── 05_trends.py
│   │   │   ├── 06_sectors.py
│   │   │   ├── 07_capital.py
│   │   │   └── 08_reports.py
│   │   └── utils/
│   │       └── db.py
│   │
│   ├── etl/
│   │   ├── loader.py
│   │   ├── normalizer.py
│   │   ├── validator.py
│   │   ├── db_loader.py
│   │   └── explore_data.py
│   │
│   ├── nlp/
│   │
│   ├── reporting/
│   │   ├── export_excel.py
│   │   ├── peer_comparison_excel.py
│   │   └── radar_charts.py
│   │
│   └── screener/
│       ├── engine.py
│       └── presets.py
│
├── tests/
│   ├── etl/
│   │   ├── test_loader.py
│   │   ├── test_normalizer.py
│   │   └── test_validator.py
│   │
│   ├── kpi/
│   │   ├── test_ratios.py
│   │   ├── test_cashflow.py
│   │   └── test_cagr.py
│   │
│   └── api/
│
├── .env
├── .gitignore
├── requirements.txt
├── nifty100.db
└── README.md
```

---

# 📊 Dataset Overview

The project uses **12 Excel datasets** as the primary source of financial information.

## Raw Datasets

| Dataset | Description |
|---------|-------------|
| companies.xlsx | Company master information |
| analysis.xlsx | Business overview |
| balancesheet.xlsx | Balance Sheet |
| cashflow.xlsx | Cash Flow Statement |
| profitandloss.xlsx | Profit & Loss Statement |
| prosandcons.xlsx | Company strengths and weaknesses |
| documents.xlsx | Annual report links |

## Supporting Datasets

| Dataset | Description |
|---------|-------------|
| financial_ratios.xlsx | Computed KPI storage |
| market_cap.xlsx | Market valuation metrics |
| peer_groups.xlsx | Industry peer mapping |
| sectors.xlsx | Sector classification |
| stock_prices.xlsx | Historical stock prices |

---

# 🗄 SQLite Database

All processed data is stored inside:

```
nifty100.db
```

The database is generated during the ETL process and serves as the central data source for analytics and dashboard modules.

### Major Tables

- companies
- balancesheet
- cashflow
- profitandloss
- financial_ratios
- analysis
- documents
- prosandcons
- sectors
- market_cap
- peer_groups
- stock_prices

---

# 🔄 ETL Pipeline

The project follows a structured ETL workflow.

## Step 1 — Extract

- Read Excel files
- Load all datasets into Pandas DataFrames

## Step 2 — Transform

- Normalize years
- Normalize company tickers
- Validate schema
- Handle missing values
- Apply data quality rules
- Validate primary and foreign keys

## Step 3 — Load

- Create SQLite schema
- Insert validated data
- Generate audit reports
- Populate supporting tables

---

# ✔ Data Quality Validation

The ETL pipeline validates data before loading it into SQLite.

Validation includes:

- Schema validation
- Primary Key validation
- Foreign Key validation
- Duplicate detection
- Missing value checks
- Financial consistency checks
- Manual review for edge cases

Generated reports include:

- `load_audit.csv`
- `validation_failures.csv`
- `ratio_edge_cases.log`

---

# ⚙ Configuration

The financial screener is fully configurable using:

```
config/screener_config.yaml
```

This configuration file defines:

- Metric thresholds
- Preset screeners
- Filter limits
- Default values

The screening engine automatically reads these settings without requiring code changes.

---

# 📈 Output Reports

The project automatically generates multiple analytical reports.

## Financial Reports

- Screener Output
- Peer Comparison Report
- Capital Allocation Report
- Validation Reports
- Valuation Summary

## Dashboard Outputs

- Interactive Plotly charts
- KPI cards
- Radar charts
- CSV downloads
- Company insights

# 🚀 Development Journey

The project was developed over **4 Agile Sprints**, with each sprint focusing on a major milestone in building the Financial Intelligence Platform.

---

# 🟢 Sprint 1 – Data Foundation

**Goal:** Build a reliable data pipeline capable of loading, validating, and storing financial data for all Nifty 100 companies.

### Completed Tasks

- Environment setup and project initialization
- Excel data loader implementation
- Data normalization
  - Year normalization
  - Company ticker normalization
- Schema validation
- 16 Data Quality (DQ) validation rules
- SQLite database schema creation
- ETL pipeline implementation
- Loading all 12 Excel datasets
- Audit report generation
- Manual data quality review
- Exploratory SQL queries

### Key Deliverables

- SQLite database (`nifty100.db`)
- ETL pipeline
- Data validation engine
- Database schema
- Load audit report
- Validation failure report

---

# 🟡 Sprint 2 – Financial Ratio Engine

**Goal:** Compute financial KPIs for every company across all available financial years.

### Profitability Metrics

- Net Profit Margin
- Operating Profit Margin
- Return on Equity (ROE)
- Return on Capital Employed (ROCE)
- Return on Assets (ROA)

### Leverage & Efficiency

- Debt-to-Equity Ratio
- Interest Coverage Ratio
- Asset Turnover
- Net Debt

### Growth Analytics

- Revenue CAGR
- PAT CAGR
- EPS CAGR

for:

- 3-Year
- 5-Year
- 10-Year periods

### Cash Flow Analytics

- Free Cash Flow
- CFO Quality Score
- CapEx Intensity
- FCF Conversion Ratio

### Capital Allocation

Implemented an 8-pattern capital allocation classification based on operating, investing, and financing cash flows.

### Additional Work

- Populated the `financial_ratios` table
- Edge-case handling
- Financial sector-specific ROCE logic
- Formula validation
- Unit testing
- Manual KPI verification

### Key Deliverables

- Financial Ratio Engine
- CAGR Engine
- Cash Flow KPI Engine
- Capital Allocation Engine
- Quality Metrics
- Ratio edge-case logging

---

# 🔵 Sprint 3 – Screener & Peer Analytics

**Goal:** Build a configurable stock screening engine and peer comparison system.

### Financial Screener

Implemented a configurable screening engine supporting custom financial filters.

Supported metrics include:

- ROE
- D/E
- Revenue CAGR
- PAT CAGR
- Free Cash Flow
- Dividend Yield
- Interest Coverage
- Asset Turnover
- Market Capitalization
- Earnings Growth
- Profitability Metrics

### Preset Screeners

Developed six predefined investment strategies:

- Quality Compounder
- Value Pick
- Growth Accelerator
- Dividend Champion
- Debt-Free Blue Chip
- Turnaround Watch

### Composite Quality Score

Built a weighted quality score using:

- Profitability
- Cash Quality
- Growth
- Leverage

### Peer Analytics

Implemented:

- Peer percentile rankings
- Peer benchmarking
- Radar charts
- Peer comparison reports

### Reporting

Generated:

- Screener reports
- Peer comparison Excel reports
- Radar chart visualizations

### Key Deliverables

- Screening Engine
- Composite Scoring Engine
- Peer Ranking Engine
- Radar Charts
- Excel Reporting

---

# 🔴 Sprint 4 – Dashboard & Valuation

**Goal:** Build an interactive Streamlit dashboard and valuation module.

### Interactive Dashboard

Developed an 8-page Streamlit application featuring:

- Home Dashboard
- Company Profile
- Financial Screener
- Peer Comparison
- Trend Analysis
- Sector Analysis
- Capital Allocation
- Annual Reports

### Dashboard Features

- Interactive company search
- KPI cards
- Plotly visualizations
- Multi-year trend analysis
- Peer benchmarking
- Sector comparison
- CSV downloads
- Responsive layout

### Valuation Module

Implemented valuation analytics including:

- Free Cash Flow Yield
- Sector Median P/E
- 5-Year Median P/E
- P/E vs Sector Median
- Valuation Flags
  - Fair
  - Discount
  - Caution

### Quality Assurance

Performed:

- Multi-company dashboard testing
- Partial-data validation
- Missing-data handling
- Screener stress testing
- Chart layout fixes
- Performance testing
- Bug fixes

### Key Deliverables

- Streamlit Dashboard
- Valuation Engine
- Valuation Reports
- Dashboard Utilities
- Integration Testing
- Project Documentation

---

# 🏆 Project Highlights

Across all four sprints, the project achieved:

- ETL pipeline for financial data ingestion
- SQLite database with validated financial data
- 50+ financial KPIs
- Configurable stock screening engine
- Composite quality scoring
- Peer percentile analysis
- Radar chart generation
- Capital allocation classification
- Valuation analytics
- Interactive Streamlit dashboard
- Automated report generation
- Comprehensive testing and validation

The final system provides a complete workflow from raw financial statements to interactive business intelligence dashboards for Nifty 100 companies.


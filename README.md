# Fiindo Recruitment Challenge – Solution by Fionn Zak

This project implements the full Fiindo recruitment challenge workflow:
Fetching financial data from the Fiindo test API → persisting it in a SQLite database → computing per-ticker metrics → aggregating them on industry level → validating logic with unit tests.

---

## Project Overview

The application performs:

1. **Data Collection**

   * Retrieves all ticker symbols
   * Fetches general profile data
   * Loads financial statements (income + balance sheet)

2. **Metric Computation**
   For the three required industries:

   * **Banks – Diversified**
   * **Software – Application**
   * **Consumer Electronics** (not present in sample data, but implemented)

   Per-ticker statistics:

   * PE Ratio (custom fallback logic if EPS is missing)
   * Revenue Growth QoQ
   * Net Income TTM
   * Debt Ratio
   * Revenue of the latest quarter

3. **Industry Aggregation**

   * Average PE Ratio
   * Average Revenue Growth
   * Sum of Revenue across all tickers in the industry

4. **Data Persistence**

   * Stored in SQLite via SQLAlchemy ORM
   * Clean schema with three tables: `symbols`, `ticker_statistics`, `industry_aggregates`

5. **Unit Testing**

   * Tests for database interactions
   * Tests for metric calculation logic

---

## Project Structure

```
fiindo-recruitment-challenge/
│
├── src/
│   ├── api_playground.py
│   ├── database.py
│   ├── models.py
│   ├── init_db.py
│   ├── load_symbols.py
│   ├── load_ticker_stats.py
│   ├── compute_industry_aggregates.py
│   ├── speedboost.py
│   └── __init__.py
│
├── tests/
│   ├── test_db.py
│   ├── test_stats.py
│
├── requirements.txt
└── README.md
```

---

## Database Schema

The solution uses **SQLite + SQLAlchemy ORM** and defines three tables:

### **1. symbols**

Stores metadata about each ticker:

* symbol
* code
* exchange
* company_name
* sector
* industry
* country
* currency
* market_cap

### **2. ticker_statistics**

Stores computed metrics:

* pe_ratio
* revenue_growth
* net_income_ttm
* debt_ratio
* revenue_last_quarter
* calculated_at

### **3. industry_aggregates**

Aggregated values per industry:

* avg_pe_ratio
* avg_revenue_growth
* sum_revenue

---

## Installation & Setup

### Clone repository

```bash
git clone <repo-url>
cd fiindo-recruitment-challenge
```

### Create virtual environment

```bash
python -m venv .venv
source .venv/bin/activate     # macOS/Linux
.\.venv\Scripts\activate      # Windows
```

### Install dependencies

```bash
pip install -r requirements.txt
```

---

## Initialize the Database

Run:

```bash
python src/init_db.py
```

This creates **fiindo_challenge.db** and all required tables.

---

## 1. Load Symbol Metadata

```bash
python src/load_symbols.py
```

This script:

* Fetches all symbols from the Fiindo API
* Fetches their general profile
* Inserts or updates the `symbols` table

---

## 2. Compute Per-Ticker Statistics

```bash
python src/load_ticker_stats.py
```

This script:

* Filters symbols belonging to the three target industries
* Fetches financial statements
* Computes PE ratio, revenue growth, TTM net income, debt ratio
* Saves results to `ticker_statistics`

Speed can be boosted beforehand using:

```bash
python src/speedboost.py
```

---

## 3. Compute Industry Aggregates

```bash
python src/compute_industry_aggregates.py
```

This computes:

* Average PE ratio
* Average revenue growth
* Total revenue

Values are stored in `industry_aggregates`.

---

## Running Tests

Tests are written using `pytest` and cover:

* Database insertion
* Metrics calculation functions

Run:

```bash
pytest -q
```

All tests should pass.

---

## Notes & Considerations

* The API sometimes returns incomplete data; PE ratio includes fallback logic (EPS diluted → EPS → netIncome/shares).
* Some industries (e.g., *Consumer Electronics*) may not exist in the test dataset; the script still handles them gracefully.
* The project avoids unnecessary re-inserts and uses **update-or-insert** behavior for symbols.

---

## Deliverables

* Fully working ETL pipeline
* SQLite database with all computed data
* Clean and documented Python code
* Automated tests
* This README with full setup instructions
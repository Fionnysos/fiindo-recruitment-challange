# **Fiindo Recruitment Challenge – Solution by Fionn Zak**

This project implements the full Fiindo recruitment workflow:

**Fetch financial data → store it in SQLite → compute ticker metrics → aggregate by industry → validate with tests → optional Dockerized pipeline.**

---

## **Learning Note**

Before this challenge I had never used **SQLAlchemy ORM** or written my own **Dockerfile**.
I knew how to *run* containers, but not how to *build* them.
While working on this project I learned:

* how SQLAlchemy ORM models, sessions, and relationships work,
* how to structure an ETL pipeline cleanly,
* how to build and run a Dockerized workflow.

I used documentation, videos, and occasional AI support to learn the needed concepts and successfully apply them.

---

## **Overview**

### **Data Collection**

* Fetch ticker symbols
* Fetch company profiles
* Load income & balance sheet statements

### **Metric Computation**

For target industries:

* Banks – Diversified
* Software – Application
* Consumer Electronics (not present in dataset, logic included)
* Consumer Cyclical (fallback due to API data)

Computed metrics:

* PE Ratio (with fallback logic)
* Revenue Growth
* Net Income (TTM)
* Debt Ratio
* Latest quarter revenue

### **Industry Aggregation**

* Average PE Ratio
* Average Revenue Growth
* Total Industry Revenue

### **Data Storage**

SQLite + SQLAlchemy ORM with tables:

* `symbols`
* `ticker_statistics`
* `industry_aggregates`

### **Testing**

`pytest` covers:

* ORM model behavior
* Metric calculation functions

### **Optional Docker Pipeline**

Container builds and runs the whole ETL flow automatically.

## **Setup**

### Create environment

```bash
pip install -r requirements.txt
```

### Initialize database

```bash
python src/init_db.py
```

### Load symbols

```bash
python src/load_symbols.py
```

### Compute ticker statistics

```bash
python src/load_ticker_stats.py
```

Optional API speed boost:

```bash
python src/speedboost.py
```

### Compute industry aggregates

```bash
python src/compute_industry_aggregates.py
```

### Run full pipeline

```bash
python src/run_pipeline.py
```

---

## **Run Tests**

```bash
pytest -q
```

---

## **Run with Docker (Optional Bonus)**

```bash
docker compose build
docker compose up
```

Runs the entire pipeline inside a container.

---

## **Summary**

This project demonstrates:

* API integration
* ETL pipeline design
* SQLAlchemy ORM for persistence
* Data analysis & aggregation
* Automated testing
* Docker-based execution

Compact, complete, and easy to run.

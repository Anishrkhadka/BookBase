# 📚 BookBase

**BookBase** is a modular, analytics-ready library management project built using the **Medallion Architecture** (Bronze, Silver, Gold layers). It uses **SQLite** to simulate a real-world data pipeline, transforming raw book metadata into business-ready insights.


## 🔧 Architecture Overview

### 🟫 Bronze Layer – Raw Ingestion
- Loads raw book metadata (`books.csv`) from the [Goodreads Dataset](https://www.kaggle.com/datasets/jealousleopard/goodreadsbooks)
- Stored in `bronze_books` without any cleaning or transformation

### 🪙 Silver Layer – Cleaned & Modelled
- Transformed and filtered into `silver_books`
- Synthetic `Members` and `BorrowingRecords` tables created and linked with foreign keys
- Trimmed text fields, validated dates, removed nulls

### 🥇 Gold Layer – Analytics & Insights
- **Views created for easy access to high-value information:**
  - `gold_top_borrowed_books`: Top 10 most borrowed books
  - `gold_top_members`: Most active library members
  - `gold_unreturned_books`: Books not yet returned
  - `gold_monthly_borrowing`: Monthly borrow trends

## 🛠️ Tech Stack

- **SQLite** – lightweight, serverless SQL engine
- **Pandas** – for CSV loading and data inspection
- **Jupyter Notebook** – development and exploration
- **Python** – data generation and logic
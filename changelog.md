# Changelog – BookBase

All notable changes to the BookBase project will be documented in this file.

---

## [0.2.0] – 2025-06-09
### Added
- Streamlit interface for viewing:
  - Books
  - Members
  - Borrowing Records
  - Top borrowed books
  - Unreturned books
- Streamlit usage documented in README
- Final project summary and architecture recap added

---

## [0.1.0] – 2025-06-08
### Added
- Initial data ingestion pipeline using Jupyter Notebooks
- SQLite setup and connection
- Medallion architecture layers:
  - Bronze: raw book data from Goodreads
  - Silver: cleaned books, synthetic Members & BorrowingRecords
  - Gold: analytical SQL views (`top borrowed`, `top members`, `unreturned`, `monthly trends`)
- Mermaid ER diagram documenting schema
- Project README with explanation and goals

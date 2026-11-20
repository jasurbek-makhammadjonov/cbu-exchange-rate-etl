# CBU Exchange Rate ETL Pipeline - Submission

Repository:
https://github.com/jasurbek-makhammadjonov/cbu-exchange-rate-etl

## What the Pipeline Does

This project implements an end-to-end ETL pipeline that retrieves official exchange rate data from the Central Bank of Uzbekistan (CBU) public API. The pipeline extracts raw exchange-rate information, transforms and cleans the data using pandas, and loads the processed records into a SQLite database for analysis.

The pipeline supports:
- Loading the latest exchange rates
- Processing a specific date
- Backfilling historical date ranges
- Running SQL-based analytical queries on the loaded data

## Architecture

The solution follows a modular ETL architecture:

CBU Public API
→ Extract Layer (`extract.py`)
→ Transform Layer (`transform.py`)
→ Load Layer (`load.py`)
→ SQLite Database
→ SQL Analytics (`analysis.sql`)

### Components

- **extract.py**: Downloads exchange-rate data from the CBU API.
- **transform.py**: Cleans data, standardizes column names, converts data types, removes duplicates, and validates records.
- **load.py**: Loads transformed data into SQLite using an idempotent loading strategy.
- **pipeline.py**: Orchestrates the complete ETL workflow and supports single-date and date-range processing.
- **analysis.sql**: Contains analytical queries for reporting and insights.

## What I Would Improve With More Time

If given more time, I would enhance the project in the following ways:

- Replace SQLite with PostgreSQL for better scalability.
- Containerize the application using Docker.
- Implement automated scheduling with Airflow or cron.
- Add CI/CD workflows using GitHub Actions.
- Introduce data quality monitoring and alerting.
- Build a Streamlit dashboard for interactive reporting and visualization.
- Increase automated test coverage across the pipeline.

## Conclusion

This project demonstrates a complete ETL workflow, including data extraction, transformation, loading, storage, and analytical reporting. The solution is modular, easy to maintain, and designed to support future enhancements.
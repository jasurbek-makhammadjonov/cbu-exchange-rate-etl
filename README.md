# CBU Exchange Rate ETL Pipeline

An end-to-end ETL pipeline that downloads the official daily exchange rates of the
Central Bank of Uzbekistan (CBU), cleans them with pandas and stores them in a
SQLite database for SQL analysis.

## Architecture

```
CBU public JSON API  ->  extract.py  ->  transform.py  ->  load.py  ->  SQLite (rates.db)  ->  sql/analysis.sql
```

| Step | File | What it does |
|------|------|--------------|
| Extract | `src/extract.py` | Downloads raw JSON for the latest or a given date |
| Transform | `src/transform.py` | Renames columns, fixes types and dates, normalises rates to one unit, drops invalid rows and duplicates |
| Load | `src/load.py` | Idempotent upsert into SQLite (re-running never creates duplicates) |
| Orchestrate | `src/pipeline.py` | CLI with latest, single-day and date-range backfill modes, logging and per-day error handling |

## Tech Stack
Python, pandas, requests, SQL (SQLite), pytest, Git

## How to Run

```bash
git clone https://github.com/jasurbek-makhammadjonov/cbu-exchange-rate-etl
cd cbu-exchange-rate-etl
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt

python -m src.pipeline                                        # latest rates
python -m src.pipeline --start 2026-09-01 --end 2026-09-30    # backfill a month
python -m pytest                                              # run tests
```

Then explore the data with the queries in `sql/analysis.sql`
(monthly averages, day-over-day change with window functions, most volatile currencies).

## Results

The pipeline loaded **23 daily rate tables** (74 currencies each) covering
28 August to 9 October 2026. All queries are in `sql/analysis.sql`.

### Example: USD/UZS change between consecutive published rates
![USD change query](docs/pictures)

### Key findings
- The official USD/UZS rate moved from **11,801.23** (28 Aug) to **11,846.57** (9 Oct),
  an increase of **45.34 UZS (+0.38%)**.
- September was stable: the USD average was **11,804.03 UZS**, and the rate stayed between
  **11,765.21** (15 Sep) and **11,839.59** (19 Sep), a range of about 0.6%.
- The largest moves between consecutive published rates in September were
  **+35.91 UZS** (18 Sep) and **-29.77 UZS** (22 Sep).
- The euro weakened against the som: average EUR/UZS was **13,601.00** in September,
  while the 9 October rate was **13,240.91** (about -2.6%).

### Data quality notes
- Monthly averages for August and October are based on a single day each, so only September is comparable.
- The change shown for 9 October covers a multi-day gap (no data loaded for 1-8 October).
- Currencies with very small rates (e.g. IRR) were excluded from the volatility ranking,
  because rounding makes their percentage changes unreliable.
	
## What I Learned
- Designing a modular ETL pipeline and making the load step idempotent
- Data cleaning and type handling with pandas
- Window functions and aggregations in SQL
- Writing unit tests for data transformations

## Next Steps
- Schedule daily runs (cron or Airflow)
- Move storage to PostgreSQL with Docker
- Add a dashboard (Streamlit)


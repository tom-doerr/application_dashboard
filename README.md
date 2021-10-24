# application_dashboard
## What is it?

This dashboard is a visualisation of the applications received by the application form.

## How to use it

1. Run `streamlit run main.py`
2. Open the dashboard at http://localhost:8501

## Data sources

* The data is stored in a PostgreSQL database.
* A connection to the database is made using the [sqlalchemy library](https://docs.sqlalchemy.org/en/13/core/engines.html).
* The data is queried using the [sqlalchemy select statement](https://docs.sqlalchemy.org/en/13/core/tutorial.html).
* The data is cached using [streamlit's caching mechanism](https://docs.streamlit.io/en/stable/api.html#display-interactive-widgets).


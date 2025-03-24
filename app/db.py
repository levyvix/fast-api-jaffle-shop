import duckdb


POPULATED_DB: duckdb.DuckDBPyConnection | None = None


def get_db() -> duckdb.DuckDBPyConnection:
    """Create in memory duckdb database from seed csv files"""
    global POPULATED_DB
    if POPULATED_DB is None:
        db = duckdb.connect(database=":memory:")
        db.sql(
            "CREATE TABLE customers AS SELECT * FROM read_csv('seed/raw_customers.csv');"
        )
        db.sql("CREATE TABLE orders AS SELECT * FROM read_csv('seed/raw_orders.csv');")
        db.sql("CREATE TABLE items AS SELECT * FROM read_csv('seed/raw_items.csv');")
        db.sql(
            "CREATE TABLE products AS SELECT * FROM read_csv('seed/raw_products.csv');"
        )
        db.sql("CREATE TABLE stores AS SELECT * FROM read_csv('seed/raw_stores.csv');")
        db.sql(
            "CREATE TABLE supplies AS SELECT * FROM read_csv('seed/raw_supplies.csv');"
        )
        POPULATED_DB = db
    return POPULATED_DB

import duckdb
import logging

logger = logging.getLogger(__name__)

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

        logger.info("Loaded seed data")

        logger.info(
            f"Customers: {db.sql('SELECT COUNT(*) FROM customers').fetchone()[0]}"
        )
        logger.info(db.sql("DESCRIBE customers").fetchall())

        logger.info(f"Orders: {db.sql('SELECT COUNT(*) FROM orders').fetchone()[0]}")
        logger.info(db.sql("DESCRIBE orders").fetchall())

        logger.info(f"Items: {db.sql('SELECT COUNT(*) FROM items').fetchone()[0]}")
        logger.info(db.sql("DESCRIBE items").fetchall())

        logger.info(
            f"Products: {db.sql('SELECT COUNT(*) FROM products').fetchone()[0]}"
        )
        logger.info(db.sql("DESCRIBE products").fetchall())

        logger.info(f"Stores: {db.sql('SELECT COUNT(*) FROM stores').fetchone()[0]}")
        logger.info(db.sql("DESCRIBE stores").fetchall())

        logger.info(
            f"Supplies: {db.sql('SELECT COUNT(*) FROM supplies').fetchone()[0]}"
        )
        logger.info(db.sql("DESCRIBE supplies").fetchall())

    return POPULATED_DB

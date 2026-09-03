import duckdb

#DB_PATH = "data/warehouse.duckdb"
DB_PATH = "data/dev.duckdb"

WAREHOUSE_DB = "data/warehouse.duckdb"

con = duckdb.connect(DB_PATH)

# Attach warehouse database
con.execute(f"""
    ATTACH '{WAREHOUSE_DB}' AS warehouse
""")

print("=== TABLES ===")
print(con.execute("SHOW TABLES").fetchall())

print("\n=== BRONZE Data ===")
print(con.execute(
    "SELECT * FROM warehouse.main.bronze_products limit 5"
).fetchall())

print("\n=== STG Data ===")
print(con.execute(
    "SELECT * FROM main.stg_products limit 5"
).fetchall())

print("\n=== SLV Data ===")
print(con.execute(
    "SELECT * FROM main.int_products limit 5"
).fetchall())

print("\n=== INGESTION LOG ===")
print(con.execute(
    "SELECT * FROM warehouse.main.ingestion_log"
).fetchall())

print("\n=== ROW COUNTS ===")

print(
    "Bronze:",
    con.execute("""
        SELECT COUNT(*)
        FROM warehouse.main.bronze_products
    """).fetchone()[0]
)

print(
    "Staging:",
    con.execute("""
        SELECT COUNT(*)
        FROM main.stg_products
    """).fetchone()[0]
)

print(
    "Intermediate:",
    con.execute("""
        SELECT COUNT(*)
        FROM main.int_products
    """).fetchone()[0]
)

print("\n=== DUPLICATE CHECK ===")

print(
    con.execute("""
        SELECT
            COUNT(*) AS total_rows,
            COUNT(DISTINCT product_id) AS unique_products,
            COUNT(*) - COUNT(DISTINCT product_id) AS duplicate_rows
        FROM main.int_products
    """).fetchone()
)

print("\n=== DATA QUALITY ===")

print(
    con.execute("""
        SELECT
            COUNT(*) AS total_rows,
            COUNT(*) FILTER (WHERE product_id IS NULL) AS null_product_id,
            COUNT(*) FILTER (WHERE price < 0) AS invalid_price,
            COUNT(*) FILTER (WHERE rating < 0 OR rating > 5) AS invalid_rating,
            COUNT(*) FILTER (WHERE stock < 0) AS invalid_stock
        FROM main.int_products
    """).fetchone()
)

con.close()
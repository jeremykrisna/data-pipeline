import duckdb

DB_PATH = "data/dev.duckdb"

con = duckdb.connect(DB_PATH)

print("DEV database created:", DB_PATH)

con.close()
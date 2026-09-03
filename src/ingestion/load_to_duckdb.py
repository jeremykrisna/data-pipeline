import duckdb
from pathlib import Path
from datetime import datetime
import pendulum

JAKARTA_TZ = pendulum.timezone("Asia/Jakarta")
BRONZE_DIR = Path("data/bronze/products")
DB_PATH = Path("data/warehouse.duckdb")


def create_ingestion_log(con):
    con.execute("""
        CREATE TABLE IF NOT EXISTS ingestion_log (
            source_file VARCHAR PRIMARY KEY,
            status VARCHAR,
            started_at TIMESTAMP,
            completed_at TIMESTAMP,
            row_count BIGINT,
            schema_changed BOOLEAN,
            columns_added VARCHAR,
            error_message VARCHAR
        )
    """)


def create_bronze_table(con, parquet_file):
    con.execute("""
        CREATE TABLE IF NOT EXISTS bronze_products AS
        SELECT *
        FROM read_parquet(?)
        LIMIT 0
    """, [str(parquet_file)])

    # Add row-level metadata columns if they do not exist yet.
    table_columns = get_table_columns(con)

    if "source_file" not in table_columns:
        con.execute("""
            ALTER TABLE bronze_products
            ADD COLUMN source_file VARCHAR
        """)

    if "snapshot_at" not in table_columns:
        con.execute("""
            ALTER TABLE bronze_products
            ADD COLUMN snapshot_at TIMESTAMP
        """)

    if "ingested_at" not in table_columns:
        con.execute("""
            ALTER TABLE bronze_products
            ADD COLUMN ingested_at TIMESTAMP
        """)


def get_table_columns(con):
    result = con.execute("""
        SELECT
            column_name,
            data_type
        FROM information_schema.columns
        WHERE table_name = 'bronze_products'
        ORDER BY ordinal_position
    """).fetchall()

    return {
        row[0]: row[1]
        for row in result
    }


def get_parquet_columns(con, parquet_file):
    result = con.execute("""
        DESCRIBE SELECT *
        FROM read_parquet(?)
    """, [str(parquet_file)]).fetchall()

    return {
        row[0]: row[1]
        for row in result
    }


def evolve_schema(con, parquet_file):
    table_columns = get_table_columns(con)
    parquet_columns = get_parquet_columns(con, parquet_file)

    # Metadata columns are managed by this loader,
    # not by the source schema.
    metadata_columns = {
        "source_file",
        "snapshot_at",
        "ingested_at"
    }

    new_columns = (
        set(parquet_columns.keys())
        - set(table_columns.keys())
        - metadata_columns
    )

    for column_name in sorted(new_columns):
        column_type = parquet_columns[column_name]

        con.execute(
            f'ALTER TABLE bronze_products '
            f'ADD COLUMN "{column_name}" {column_type}'
        )

        print(
            f"Schema evolution: added column "
            f"{column_name} ({column_type})"
        )

    return new_columns


def is_processed(con, parquet_file):
    result = con.execute("""
        SELECT status
        FROM ingestion_log
        WHERE source_file = ?
    """, [str(parquet_file)]).fetchone()

    return result is not None and result[0] == "SUCCESS"


def get_snapshot_time(parquet_file):
    """
    Extract snapshot timestamp from the file path.

    Example:
        data/bronze/products/2026-09-03/products_090530.parquet

    Returns:
        2026-09-03 09:05:30
    """

    date_part = parquet_file.parent.name
    time_part = parquet_file.stem.replace("products_", "")

    #return datetime.strptime(
    #    f"{date_part} {time_part}",
    #    "%Y-%m-%d %H%M%S"
    #)
    return JAKARTA_TZ.convert(
        datetime.strptime(
            f"{date_part} {time_part}",
            "%Y-%m-%d %H%M%S"
        )
    )


def build_insert_query(con, parquet_file):
    """
    Build an explicit INSERT statement instead of SELECT *.

    This makes the loader safer when the Bronze schema evolves.
    """

    table_columns = get_table_columns(con)
    parquet_columns = get_parquet_columns(con, parquet_file)

    metadata_columns = {
        "source_file",
        "snapshot_at",
        "ingested_at"
    }

    source_table_columns = [
        column
        for column in table_columns
        if column not in metadata_columns
    ]

    target_columns = [
        f'"{column}"'
        for column in source_table_columns
    ]

    target_columns.extend([
        '"source_file"',
        '"snapshot_at"',
        '"ingested_at"'
    ])

    select_columns = []

    for column in source_table_columns:
        if column in parquet_columns:
            select_columns.append(f'"{column}"')
        else:
            column_type = table_columns[column]

            select_columns.append(
                f'CAST(NULL AS {column_type}) AS "{column}"'
            )

    select_columns.extend([
        "? AS source_file",
        "? AS snapshot_at",
        "? AS ingested_at"
    ])

    query = f"""
        INSERT INTO bronze_products (
            {", ".join(target_columns)}
        )
        SELECT
            {", ".join(select_columns)}
        FROM read_parquet(?)
    """

    return query


def load_parquet(con, parquet_file):
    print(f"Processing: {parquet_file}")

    if is_processed(con, parquet_file):
        print("Already processed. Skipping.")
        return

    create_bronze_table(con, parquet_file)

    new_columns = evolve_schema(con, parquet_file)

    snapshot_at = get_snapshot_time(parquet_file)
    #ingested_at = datetime.now()
    ingested_at = datetime.now(JAKARTA_TZ)

    con.execute("BEGIN")

    try:
        insert_query = build_insert_query(con, parquet_file)

        con.execute(
            insert_query,
            [
                str(parquet_file),
                snapshot_at,
                ingested_at,
                str(parquet_file)
            ]
        )

        row_count = con.execute("""
            SELECT COUNT(*)
            FROM read_parquet(?)
        """, [str(parquet_file)]).fetchone()[0]

        con.execute("""
            INSERT OR REPLACE INTO ingestion_log (
                source_file,
                status,
                started_at,
                completed_at,
                row_count,
                schema_changed,
                columns_added,
                error_message
            )
            VALUES (
                ?,
                'SUCCESS',
                ?,
                CURRENT_TIMESTAMP,
                ?,
                ?,
                ?,
                NULL
            )
        """, [
            str(parquet_file),
            ingested_at,
            row_count,
            len(new_columns) > 0,
            ", ".join(sorted(new_columns))
        ])

        con.execute("COMMIT")

        print(
            f"Loaded successfully: "
            f"{row_count} rows, "
            f"snapshot={snapshot_at}"
        )

    except Exception as e:
        con.execute("ROLLBACK")

        con.execute("""
            INSERT OR REPLACE INTO ingestion_log (
                source_file,
                status,
                started_at,
                completed_at,
                row_count,
                schema_changed,
                columns_added,
                error_message
            )
            VALUES (
                ?,
                'FAILED',
                ?,
                CURRENT_TIMESTAMP,
                0,
                ?,
                ?,
                ?
            )
        """, [
            str(parquet_file),
            ingested_at,
            len(new_columns) > 0,
            ", ".join(sorted(new_columns)),
            str(e)
        ])

        print(f"Failed: {e}")
        raise


def main():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    parquet_files = sorted(
        BRONZE_DIR.glob("*/*.parquet")
    )

    if not parquet_files:
        print("No Parquet files found.")
        return

    con = duckdb.connect(DB_PATH)

    try:
        create_ingestion_log(con)

        for parquet_file in parquet_files:
            load_parquet(con, parquet_file)

    finally:
        con.close()


if __name__ == "__main__":
    main()

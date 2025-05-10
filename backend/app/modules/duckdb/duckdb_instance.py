import duckdb

database_url = ':memory:'  # For prod -> 'duck_db.duckdb'

def get_duckdb_connection():
    conn = duckdb.connect(database=database_url)
    try:
        yield conn
    finally:
        conn.close()

from typing import Annotated

import duckdb
from fastapi import Depends

database_url = 'duck_db.duckdb'  # For prod -> 'duck_db.duckdb'

def get_duckdb_connection():
    conn = duckdb.connect(database=database_url)
    try:
        yield conn
    finally:
        conn.close()

DuckDBDep = Annotated[duckdb.DuckDBPyConnection, Depends(get_duckdb_connection)]

def setup_db(duck):
    duck.query("INSTALL spatial;")
    duck.query("LOAD spatial;")
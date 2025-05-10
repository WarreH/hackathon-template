from duckdb import DuckDBPyConnection
import polars as pl

from app.modules.duckdb.dataset_to_duckdb import SOURCE_DATASET
from app.modules.location.location_py_model import PyLocation


def proximity_algorithm(duck: DuckDBPyConnection,
                        current_pos: PyLocation,
                        long_lat_max: float) -> pl.DataFrame:
    stmt = f"""
    SELECT 
        id,
        type,
        lon,
        lat,
        tags,
    FROM {SOURCE_DATASET}
    WHERE 
        -- Filter out 'ways' or 'relation'
        type == $node_type 
        -- Filter on distance
        AND ST_Distance(
            ST_Point(lon, lat), 
            ST_Point({current_pos.longitude}, {current_pos.latitude})
        ) <= {long_lat_max}
    """
    filter_weg_set = {
        '%"source": "PSG(could be inaccurately)"%',
        '%"highway":%',
    }
    for filter_weg in filter_weg_set:
        stmt += f"""\n    AND tags NOT LIKE '{filter_weg}'"""

    filter_include_set = {
        '%"name":%'
    }
    for filter_include in filter_include_set:
        stmt += f"""\n    AND tags LIKE '{filter_include}'"""

    params = {
        "node_type": "node"
    }
    return duck.execute(stmt, params).pl()

import json

from duckdb import DuckDBPyConnection
import polars as pl

from app.modules.location.location_py_model import PyLocation
from app.modules.recommendation.algorithms.proximity_algorithm import proximity_algorithm
from app.modules.recommendation.recommendation_py_models import PyCandidateResult, PyRecQuery


def candidate_computation(duck: DuckDBPyConnection,
                          user_query_param: PyRecQuery,
                          candidate_n: int) -> list[PyCandidateResult]:
    # -----
    # Algorithm Parameters
    long_lat_max: float = 100.0  # In meters

    # TODO - everything lol
    batch_one: pl.DataFrame = proximity_algorithm(duck=duck,
                                                  current_pos=user_query_param.location,
                                                  long_lat_max=long_lat_max)

    # -----
    # Assemble into candidates
    candidates: list[PyCandidateResult] = []

    batch_two = batch_one.head(10)

    for row in batch_two.to_dicts():
        labels = json.loads(row['tags'])

        candidates.append(
            PyCandidateResult(
                location=PyLocation(
                    longitude=row["lon"],
                    latitude=row["lat"]
                ),
                osm_tags=labels,
            )
        )

    # Return
    return candidates

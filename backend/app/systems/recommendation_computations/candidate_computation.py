import json
from cmath import polar

from duckdb import DuckDBPyConnection
import polars as pl

from app.modules.location.location_py_model import PyLocation
from app.modules.recommendation.algorithms.proximity_algorithm import proximity_algorithm
from app.modules.recommendation.recommendation_py_models import PyCandidateResult, PyRecQuery
from app.modules.recommendation.algorithms.embedding_generator import apply_cosine_simularity

def candidate_computation(duck: DuckDBPyConnection,
                          user_query_param: PyRecQuery,
                          candidate_n: int) -> list[PyCandidateResult]:
    # -----
    # Algorithm Parameters
    max_distance_meters: float = 0.002  # 0.001 is approx 100m

    # -----
    # Filtering based on distance and some "this won't be useful" tags
    batch_one: pl.DataFrame = proximity_algorithm(duck=duck,
                                                  current_pos=user_query_param.location,
                                                  max_distance_meters=max_distance_meters)

    # -----
    # Applying cosine similarity
    batch_two = apply_cosine_simularity(batch_one.to_pandas(),user_query_param.interests)
    batch_two = pl.from_pandas(batch_two)
    # batch_two = batch_one

    # -----
    # Assemble return
    candidates: list[PyCandidateResult] = []
    for row in batch_two.to_dicts():
        labels = json.loads(row['tags'])

        candidates.append(
            PyCandidateResult(
                location=PyLocation(
                    longitude=row["lon"],
                    latitude=row["lat"]
                ),
                osm_tags=labels,
                distance=row["distance"]
            )
        )

    # Return
    return candidates

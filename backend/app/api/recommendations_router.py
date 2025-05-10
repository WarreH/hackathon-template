from fastapi import APIRouter, Query

from app.modules.duckdb.duckdb_instance import DuckDBDep
from app.modules.recommendation.recommendation_py_models import PyRecommendedResult, PyRecQuery
from app.systems.recommendation_computations.recommendation_computation import recommend_locations

rec_router = APIRouter(prefix="/recommend", tags=["recommend"])

@rec_router.post("")
async def get_recommendations(duck: DuckDBDep,
                              user_query_param: PyRecQuery,
                              limit: int = Query(default=10)) -> list[PyRecommendedResult]:
    return await recommend_locations(duck=duck,
                                     user_query_param=user_query_param,
                                     n_recommendations=limit)

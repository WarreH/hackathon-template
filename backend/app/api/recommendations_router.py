from fastapi import APIRouter, Query

from app.modules.recommendation.recommendation_py_models import PyRecommendedResult, PyRecQuery
from app.systems.recommendation_computations.recommendation_computation import recommend_locations

rec_router = APIRouter(prefix="/recommend", tags=["recommend"])

@rec_router.get("")
async def get_recommendations(user_query_param: PyRecQuery,
                              limit = Query(default=10, ge=1, le=15)) -> list[PyRecommendedResult]:
    return await recommend_locations(user_query_param=user_query_param,
                                     n_recommendations=limit)

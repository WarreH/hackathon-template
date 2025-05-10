from fastapi import APIRouter
from pydantic import BaseModel

from app.modules.location.location_py_model import PyLocation
from app.modules.recommendation.recommendation_py_models import RecommendedResult


class PyRecQuery(BaseModel):
    location: PyLocation
    interests: list[str]

rec_router = APIRouter(prefix="/recommend", tags=["recommend"])

@rec_router.get("")
async def get_recommendations(user_query_param: PyRecQuery) -> list[RecommendedResult]:
    return []

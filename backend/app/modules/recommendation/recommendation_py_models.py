from typing import Optional

from pydantic import BaseModel, Field

from app.modules.location.location_py_model import PyLocation


class PyRecQuery(BaseModel):
    """
    Input for recommendation generation
    """
    location: PyLocation

    user_identifier: Optional[str] = None
    interests: list[str]

class PyCandidateResult(BaseModel):
    """
    All options reduced to a couple, this recommendation
    """
    location: PyLocation
    distance: float

    osm_tags: dict

class PyRecommendedResult(PyCandidateResult):
    """
    API RESULT FOR A RECOMMENDATION QUERY

    INHERITS FROM CANDIDATE GENERATION
    """

    # Resulting rankings
    score: float = Field(ge=0,
                         description="Resulting score of the recommendation"
                         )
    ensemble_scores: dict[str, float] = Field(
        description="For each algorithm used, the score for the location recommended"
    )
    description: str
    name: str
    label: str

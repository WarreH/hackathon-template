from pydantic import BaseModel

from app.modules.location.location_py_model import PyLocation


class RecommendedResult(BaseModel):
    """
    API RESULT FOR A RECOMMENDATION QUERY
    """
    location: PyLocation
    ...
    # todo alle fields toevoegen voor een recommendatie
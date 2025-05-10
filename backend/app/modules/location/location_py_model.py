from pydantic import BaseModel


class PyLocation(BaseModel):
    longitude: float
    latitude: float

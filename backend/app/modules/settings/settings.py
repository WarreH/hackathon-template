from typing import Literal

from pydantic import BaseModel


class Settings(BaseModel):
    environment: Literal["development", "staging", "production"]

    @property
    def is_debug(self) -> bool:
        return self.environment == "development"

settings = Settings(
    environment="development",
)
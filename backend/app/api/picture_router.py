from typing import Any

from fastapi import APIRouter

picture_router = APIRouter(prefix="/picture", tags=["picture"])

@picture_router.post("")
async def post_picture() -> str:
    """

    :return: Picture identifier
    """
    return ""

@picture_router.get("/{picture_identifier}")
def get_picture(picture_identifier: str) -> Any:
    """

    :param picture_identifier:
    :return: Picture
    """
    return

@picture_router.get("/experience/{user_identifier}")
async def query_experience(user_identifier: str) -> list[str]:
    """

    :param user_identifier
    :return: list of picture identifiers
    """
    return []

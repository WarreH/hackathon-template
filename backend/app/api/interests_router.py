from fastapi import APIRouter

from app.systems.interests_computation import computer_interests_options

interest_router = APIRouter(prefix="/interests", tags=["interests"])

@interest_router.get("")
async def get_interest_options() -> list[str]:
    """
    Returns options for interests

    :return:
    """
    return await computer_interests_options()

from fastapi import APIRouter

interest_router = APIRouter(prefix="/interests", tags=["interests"])

@interest_router.get("")
async def get_interest_options() -> list[str]:
    """
    Returns options for interests

    :return:
    """
    return []

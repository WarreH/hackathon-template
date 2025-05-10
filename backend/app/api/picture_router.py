from io import BytesIO
from sys import exception
from typing import Any

from fastapi import APIRouter, Path, File, UploadFile
from starlette.exceptions import HTTPException
from starlette.responses import StreamingResponse

from app.modules.picture.picture_interface_dependency import PictureManagerDep

picture_router = APIRouter(prefix="/picture", tags=["picture"])

@picture_router.post("/{user_identifier}")
async def post_picture(picture_manager: PictureManagerDep,
                       user_identifier: str = Path(),
                       file: UploadFile = File(...),
                       ) -> str:
    """
    :return: Picture identifier
    """
    # Validation
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image.")

    # Attempt to store file
    try:
        file_bytes = await file.read()
        file_identifier = await picture_manager.upload_picture(user_identifier=user_identifier,
                                                               file_name=file.filename,
                                                               file_bytes=file_bytes)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return file_identifier

@picture_router.get("/{picture_identifier}")
async def get_picture(picture_manager: PictureManagerDep,
                picture_identifier: str) -> Any:
    """

    :param picture_manager:
    :param picture_identifier:
    :return: Picture
    """
    try:
        file_bytes: bytes = await picture_manager.get_picture(file_identifier=picture_identifier)
        extension = picture_identifier.split(".")[-1]
        return StreamingResponse(BytesIO(file_bytes), media_type=f"image/{extension}")
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@picture_router.get("/experience/{user_identifier}")
async def query_experience(picture_manager: PictureManagerDep,
                           user_identifier: str) -> list[str]:
    """

    :param picture_manager:
    :param user_identifier
    :return: list of picture identifiers
    """
    return await picture_manager.query_pictures_identifiers(user_identifier=user_identifier)

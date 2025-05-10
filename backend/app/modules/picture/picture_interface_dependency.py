import os
from typing import Annotated, Optional

from fastapi import HTTPException
from fastapi.params import Depends

class LocalStorage:
    def __init__(self, directory_name: str):
        # Check if directory exists
        self.directory_name = directory_name

        if not os.path.exists(self.directory_name):
            os.mkdir(self.directory_name)

    def list_files(self) -> list[str]:
        return os.listdir(self.directory_name)

    def store_bytes(self, file_name: str, file_bytes: bytes):
        file_path = os.path.join(self.directory_name, file_name)

        # If file exists we will overwrite
        with open(file_path, 'wb') as f:
            f.write(file_bytes)

    def load_bytes(self, file_name) -> Optional[bytes]:
        file_path = os.path.join(self.directory_name, file_name)

        # Check if file exists
        if not os.path.exists(file_path):
            return None

        # Load and return
        with open(file_path, 'rb') as f:
            return f.read()


class PictureManager:
    def __init__(self, storage):
        self.storage = storage

    async def upload_picture(self,
                             user_identifier: str,
                             file_name: str,
                             file_bytes: bytes) -> str:
        file_identifier = user_identifier.lower() + "_" + file_name.lower()
        self.storage.store_bytes(file_name=file_identifier, file_bytes=file_bytes)
        return file_identifier

    async def get_picture(self, file_identifier: str) -> bytes :
        file_opt = self.storage.load_bytes(file_identifier)
        if not file_opt:
            raise HTTPException(status_code=404, detail="File not found")
        return file_opt

    async def query_pictures_identifiers(self, user_identifier) -> list[str]:
        filenames = self.storage.list_files()
        return list(filter(lambda filename: filename.startswith(user_identifier), filenames))

    async def __call__(self):
        return self

PictureManagerDep = Annotated[PictureManager, Depends(PictureManager(LocalStorage("/tmp/pictures")))]

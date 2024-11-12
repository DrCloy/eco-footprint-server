import base64
from bson import ObjectId
from fastapi import HTTPException, UploadFile

from pymongo.database import Database

from core.model import FileData
from core.repo import FileRepository


class FileMongoRepo(FileRepository):
    def __init__(self, db: Database):
        super().__init__()
        self._db = db
        self._collection = db["files"]

    def createFile(self, file: UploadFile, userId: str) -> FileData:
        fileData = FileData(
            id=str(ObjectId()),
            owner=userId,
            name=file.filename,
            contentType=file.content_type,
            size=file.size,
            file=base64.b64encode(file.file.read()).decode("utf-8")
        )

        self._collection.insert_one(fileData.model_dump())

        return fileData

    def getFile(self, fileId: str) -> FileData:
        file = self._collection.find_one({"id": fileId})
        if file:
            return FileData(
                id=file["id"],
                owner=file["owner"],
                name=file["name"],
                contentType=file["contentType"],
                size=file["size"],
                file=base64.b64decode(file["file"])
            )
        else:
            raise HTTPException(status_code=404, detail="File not found")

    def updateFile(self, file: UploadFile, fileData: FileData) -> FileData:
        fileData.name = file.filename
        fileData.contentType = file.content_type
        fileData.size = file.size
        fileData.file = base64.b64encode(file.file.read()).decode("utf-8")

        self._collection.update_one({"id": fileData.id}, {"$set": fileData.model_dump()})

        return fileData

    def deleteFile(self, fileId: str) -> bool:
        result = self._collection.delete_one({"id": fileId})
        return result.deleted_count > 0

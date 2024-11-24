import base64
from bson import ObjectId
from fastapi import HTTPException, UploadFile

from pymongo.database import Database

from core.model import FileData
from core.repo import FileRepository


class FileMongoRepo(FileRepository):
    """
    Implementation of FileRepository using MongoDB
    """

    def __init__(self, db: Database):
        super().__init__()
        self._db = db
        self._collection = db["files"]

    def createFile(self, file: UploadFile, userId: str) -> FileData:
        """
        Create a new file

        Args:
            file (UploadFile): File to be uploaded
            userId (str): User ID of the owner of the file

        Returns:
            FileData: FileData object of the uploaded file
        """
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
        """
        Get file by ID

        Args:
            fileId (str): ID of the file

        Returns:
            FileData: FileData object of the file if found, None otherwise
        """
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
            return None

    def updateFile(self, file: UploadFile, fileData: FileData) -> FileData:
        """
        Update file data with new file

        Args:
            file (UploadFile): New file to be uploaded
            fileData (FileData): FileData object to be updated

        Returns:
            FileData: FileData object of the updated file if successful, None otherwise
        """
        fileData.name = file.filename
        fileData.contentType = file.content_type
        fileData.size = file.size
        fileData.file = base64.b64encode(file.file.read()).decode("utf-8")

        self._collection.update_one({"id": fileData.id}, {"$set": fileData.model_dump()})

        newFile = self._collection.find_one({"id": fileData.id})

        if fileData == newFile:
            return FileData(
                id=newFile["id"],
                owner=newFile["owner"],
                name=newFile["name"],
                contentType=newFile["contentType"],
                size=newFile["size"],
                file=base64.b64decode(newFile["file"])
            )
        else:
            return None

    def deleteFile(self, fileId: str) -> bool:
        """
        Delete file by ID

        Args:
            fileId (str): ID of the file

        Returns:
            bool: True if file is deleted, False otherwise
        """
        result = self._collection.delete_one({"id": fileId})
        return result.deleted_count > 0

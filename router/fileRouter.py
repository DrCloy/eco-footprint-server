from fastapi import UploadFile, HTTPException, Request, APIRouter, Response

from core.model import FileData
from core.repo import UserRepository, FileRepository


class FileRouter(APIRouter):
    """
    FileRouter class

    This class is a router class for file-related API endpoints.
    """

    def __init__(self, userRepo: UserRepository, fileRepo: FileRepository):
        super().__init__(prefix="/file")
        self._userRepo = userRepo
        self._fileRepo = fileRepo

        self.add_api_route('/create', self._createFile, methods=['POST'])
        self.add_api_route('/{fileId}', self._getFile, methods=['GET'])
        self.add_api_route('/update/{fileId}', self._updateFile, methods=['PUT'])
        self.add_api_route('/delete/{fileId}', self._deleteFile, methods=['DELETE'])

    def _createFile(self, isPrivate: bool, file: UploadFile, request: Request) -> FileData:
        """
        Create a new file
        This method creates a new file with the given file.

        Args:
            file (UploadFile): The file to create
            request (Request): The request object

        Raises:
            HTTPException(status_code=400): If no file is provided
            HTTPException(status_code=403): If the user is not authenticated

        Returns:
            FileData: The created file
        """
        if not request.state.auth:
            raise HTTPException(status_code=403, detail="Unauthorized")
        if not request.state.auth.get("sub"):
            raise HTTPException(status_code=403, detail="Unauthorized")

        userId = request.state.auth.get("sub")
        if not self._userRepo.getUser(userId):
            raise HTTPException(status_code=403, detail="Unauthorized")

        return self._fileRepo.createFile(file, userId, isPrivate)

    def _getFile(self, fileId: str, request: Request):
        """
        Get a file by ID
        This method gets a file by its ID.

        Args:
            fileId (str): The ID of the file
            request (Request): The request object

        Raises:
            HTTPException(status_code=403): If the user is not authenticated
            HTTPException(status_code=404): If the file is not found

        Returns:
            Response: The file
        """
        if not request.state.auth:
            raise HTTPException(status_code=403, detail="Unauthorized")
        if not request.state.auth.get("sub"):
            raise HTTPException(status_code=403, detail="Unauthorized")

        user = self._userRepo.getUser(request.state.auth.get("sub"))
        if not user:
            raise HTTPException(status_code=403, detail="Unauthorized")

        file = self._fileRepo.getFile(fileId)
        if not file:
            raise HTTPException(status_code=404, detail="File not found")
        if file.isPrivate and file.owner != user.id:
            raise HTTPException(status_code=403, detail="Unauthorized")

        return Response(content=file.file, media_type=file.contentType)

    def _updateFile(self, fileId: str, file: UploadFile, request: Request) -> FileData:
        """
        Update a file
        This method updates a file with the given file.

        Args:
            fileId (str): The ID of the file
            file (UploadFile): The file to update
            request (Request): The request object

        Raises:
            HTTPException(status_code=400): If no file is provided
            HTTPException(status_code=403): If the user is not authenticated

        Returns:
            FileData: The updated file
        """
        if not request.state.auth:
            raise HTTPException(status_code=403, detail="Unauthorized")
        if not request.state.auth.get("sub"):
            raise HTTPException(status_code=403, detail="Unauthorized")

        userId = request.state.auth.get("sub")
        if not self._userRepo.getUser(userId):
            raise HTTPException(status_code=403, detail="Unauthorized")

        fileData = self._fileRepo.getFile(fileId)
        if not fileData:
            raise HTTPException(status_code=404, detail="File not found")
        if fileData.owner != userId:
            raise HTTPException(status_code=403, detail="Unauthorized")

        return self._fileRepo.updateFile(file, self._fileRepo.getFile(fileId))

    def _deleteFile(self, fileId: str, request: Request) -> bool:
        """
        Delete a file
        This method deletes a file by its ID.

        Args:
            fileId (str): The ID of the file
            request (Request): The request object

        Raises:
            HTTPException(status_code=403): If the user is not authenticated

        Returns:
            bool: True if the file was deleted, False otherwise
        """
        if not request.state.auth:
            raise HTTPException(status_code=403, detail="Unauthorized")
        if not request.state.auth.get("sub"):
            raise HTTPException(status_code=403, detail="Unauthorized")
        if not request.state.auth.get("sub") == self._fileRepo.getFile(fileId).owner:
            raise HTTPException(status_code=403, detail="Unauthorized")

        return self._fileRepo.deleteFile(fileId)

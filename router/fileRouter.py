from fastapi import UploadFile, File, HTTPException, Request, APIRouter, Response

from core.model import UserItem, FileData
from core.repo import UserRepository, FileRepository


class FileRouter(APIRouter):
    def __init__(self, userRepo: UserRepository, fileRepo: FileRepository):
        super().__init__(prefix="/file")
        self._userRepo = userRepo
        self._fileRepo = fileRepo

        self.add_api_route('/create', self.createFile, methods=['POST'])
        self.add_api_route('/{fileId}', self.getFile, methods=['GET'])
        self.add_api_route('/update/{fileId}', self.updateFile, methods=['PUT'])
        self.add_api_route('/delete/{fileId}', self.deleteFile, methods=['DELETE'])

    def createFile(self, file: UploadFile, request: Request) -> FileData:
        if not file:
            raise HTTPException(status_code=400, detail="No file provided")
        if not request.state.auth:
            raise HTTPException(status_code=403, detail="Unauthorized")

        return self._fileRepo.createFile(file, request.state.auth.get("aud"))

    def getFile(self, fileId: str, request: Request):
        user = self._userRepo.getUser(request.state.auth.get("aud"))
        if not user:
            raise HTTPException(status_code=403, detail="Unauthorized")
        file = self._fileRepo.getFile(fileId)
        if not file:
            raise HTTPException(status_code=404, detail="File not found")
        if file.owner != user.id:
            raise HTTPException(status_code=403, detail="Unauthorized")

        return Response(content=file.file, media_type=file.contentType)

    def updateFile(self, fileId: str, file: UploadFile, request: Request) -> FileData:
        if not file:
            raise HTTPException(status_code=400, detail="No file provided")
        if not request.state.auth:
            raise HTTPException(status_code=403, detail="Unauthorized")
        if not request.state.auth.get("aud") == self._fileRepo.getFile(fileId).owner:
            raise HTTPException(status_code=403, detail="Unauthorized")

        return self._fileRepo.updateFile(file, self._fileRepo.getFile(fileId))

    def deleteFile(self, fileId: str, request: Request) -> bool:
        if not request.state.auth.get("aud") == self._fileRepo.getFile(fileId).owner:
            raise HTTPException(status_code=403, detail="Unauthorized")

        return self._fileRepo.deleteFile(fileId)

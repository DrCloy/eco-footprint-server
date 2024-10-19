from fastapi import APIRouter
from core.repo import UserRepository
from repo.user_test import UserTestRepo

userRouter = APIRouter()

userRepo: UserRepository = UserTestRepo()


userRouter.add_api_route('/{user_id}', userRepo.get_user, methods=['GET'])

# Import libraries and modules
from typing import *
from fastapi import FastAPI, responses, HTTPException, APIRouter, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer

import os
import pymongo

from dotenv import load_dotenv

from middleware.authParser import AuthParser
from core.repo import UserRepository, FileRepository, RewardRepository, CouponRepository
from repo.userMongo import UserMongoRepo
from repo.fileMongo import FileMongoRepo
from repo.rewardMongo import RewardMongoRepo
from repo.couponMongo import CouponMongoRepo
from router.userRouter import UserRouter
from router.fileRouter import FileRouter
from router.rewardRouter import RewardRouter

# Load environment variables
load_dotenv(verbose=True, dotenv_path=".env.development", override=True)

MONGO_HOST = os.getenv("MONGO_HOST")
MONGO_PORT = os.getenv("MONGO_PORT")
MONGO_USER = os.getenv("MONGO_USER")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
MONGO_DB = os.getenv("MONGO_DB")

########## MongoDB Connection ##########
client = pymongo.MongoClient(host=MONGO_HOST, port=int(MONGO_PORT), username=MONGO_USER, password=MONGO_PASSWORD)
db = client[MONGO_DB]

########## Dependency Injection ##########
user_repo: UserRepository = UserMongoRepo(db)
file_repo: FileRepository = FileMongoRepo(db)
reward_repo: RewardRepository = RewardMongoRepo(db)
coupon_repo: CouponRepository = CouponMongoRepo(db)

user_router = UserRouter(user_repo)
file_router = FileRouter(user_repo, file_repo)
reward_router = RewardRouter(user_repo, reward_repo, coupon_repo, file_repo)

########## FastAPI App ##########
security = HTTPBearer()
app = FastAPI(title="Eco-Footprint API", version="0.1", dependencies=[Depends(security)])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(AuthParser)

########## Error Handlers ##########


@app.exception_handler(HTTPException)
def http_exception_handler(request, exc):
    return responses.JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )


########## Add routers ##########
app_router = APIRouter(prefix="/api")
app_router.include_router(user_router, tags=["User"])
app_router.include_router(file_router, tags=["File"])
app_router.include_router(reward_router, tags=["Reward"])

app.include_router(app_router)

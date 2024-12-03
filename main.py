# Import libraries and modules
from typing import *
from fastapi import FastAPI, responses, HTTPException, APIRouter, Depends
from fastapi.middleware.cors import CORSMiddleware

import os
import pymongo

from dotenv import load_dotenv

from util.authParser import AuthParser
from core.repo import UserRepository, FileRepository, RewardRepository, CouponRepository, DonationRepository, ChallengeRepository
from repo.userMongo import UserMongoRepo
from repo.fileMongo import FileMongoRepo
from repo.rewardMongo import RewardMongoRepo
from repo.couponMongo import CouponMongoRepo
from repo.donationMongo import DonationMongoRepo
from repo.challengeMongo import ChallengeMongoRepo
from router.userRouter import UserRouter
from router.fileRouter import FileRouter
from router.tempRewardRouter import RewardRouter
from router.donationRouter import DonationRouter
from router.challengeRouter import ChallengeRouter
from router.adRouter import AdRouter
from util.adVerifier import AdVerifier

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
donation_repo: DonationRepository = DonationMongoRepo(db)
challenge_repo: ChallengeRepository = ChallengeMongoRepo(db)

ad_verifier: AdVerifier = AdVerifier()

user_router = UserRouter(user_repo, ad_verifier)
file_router = FileRouter(user_repo, file_repo)
reward_router = RewardRouter(user_repo, reward_repo, coupon_repo, file_repo)
donation_router = DonationRouter(user_repo, donation_repo)
challenge_router = ChallengeRouter(user_repo, challenge_repo, file_repo)
ad_router = AdRouter(user_repo, ad_verifier)

########## FastAPI App ##########
security = AuthParser()
app = FastAPI(title="Eco-Footprint API", version="0.1", dependencies=[Depends(security)], docs_url="/balloon/docs")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
app_router.include_router(donation_router, tags=["Donation"])
app_router.include_router(challenge_router, tags=["Challenge"])
app_router.include_router(ad_router, tags=["Ad"])

app.include_router(app_router)

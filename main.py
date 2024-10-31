# Import libraries and modules
from typing import *
from fastapi import FastAPI, responses, HTTPException, APIRouter
from fastapi.middleware.cors import CORSMiddleware

import os
import pymongo

from dotenv import load_dotenv

from core.repo import UserRepository

from repo.user_mongo import UserMongoRepo
from repo.donation_test import DonationTestRepo

from router.userRouter import UserRouter
from router.donationRouter import create_donation_router

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

user_router = UserRouter(db, user_repo)

########## FastAPI App ##########
app = FastAPI(title="Eco-Footprint API", version="0.1")

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
app_router.include_router(user_router)

app.include_router(app_router)

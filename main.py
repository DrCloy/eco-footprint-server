from typing import *
from fastapi import FastAPI, responses, HTTPException, APIRouter
from fastapi.middleware.cors import CORSMiddleware

import pymongo

from core.repo import UserRepository

from repo.user_mongo import UserMongoRepo
from repo.donation_test import DonationTestRepo

from router.userRouter import UserRouter
from router.donationRouter import create_donation_router

########## MongoDB Connection ##########
client = pymongo.MongoClient(host="localhost", port=27017, username="admin", password="admin")
db = client.test

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

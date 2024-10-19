from typing import *
from fastapi import FastAPI, responses, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from core.repo import UserRepository, DonationRepository

from repo.user_test import UserTestRepo
from repo.donation_test import DonationTestRepo

from routers.userRouter import create_user_router
from routers.donationRouter import create_donation_router

########## Dependency Injection ##########
user_repo: UserRepository = UserTestRepo()
donation_repo: DonationRepository = DonationTestRepo()


user_router = create_user_router(user_repo)
donation_router = create_donation_router(donation_repo)


app = FastAPI(root_path="/api", title="Eco-Footprint API", version="0.1")

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
app.include_router(user_router)
app.include_router(donation_router)

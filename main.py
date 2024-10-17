from typing import *
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers.userRouter import userRouter

app = FastAPI(root_path="/api")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


########## Add routers ##########
app.include_router(userRouter, prefix="/user", tags=["user"])

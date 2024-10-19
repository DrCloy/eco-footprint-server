from typing import *
from fastapi import FastAPI, responses, HTTPException
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

########## Error Handlers ##########


@app.exception_handler(HTTPException)
def http_exception_handler(request, exc):
    return responses.JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )


########## Add routers ##########
app.include_router(userRouter, prefix="/user", tags=["user"])

import pymongo

from fastapi import HTTPException

from core.model import UserData
from core.repo import UserRepository


class UserMongoRepo(UserRepository):
    def __init__(self, client: pymongo.MongoClient):
        self.client = pymongo.MongoClient()
        super().__init__()
        self.db = client.admin

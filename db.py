from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()
MONGO_URL = os.getenv("MONGO_DB")


client = AsyncIOMotorClient(MONGO_URL)
db = client["vocab"]
collection = db["words"]
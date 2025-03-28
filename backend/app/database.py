import os
from motor.motor_asyncio import AsyncIOMotorClient

# MongoDB connection
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = AsyncIOMotorClient(MONGO_URI)
db = client.uploader
uploads_collection = db.uploads

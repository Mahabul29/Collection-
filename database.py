from motor.motor_asyncio import AsyncIOMotorClient
from config import settings

class Database:
    client: AsyncIOMotorClient = None

db = Database()

async def connect_to_mongo():
    db.client = AsyncIOMotorClient(settings.MONGO_URI)
    print("Connected to MongoDB successfully.")

async def close_mongo_connection():
    if db.client:
        db.client.close()
        print("Closed MongoDB connection.")

def get_database():
    return db.client.get_default_database()
  

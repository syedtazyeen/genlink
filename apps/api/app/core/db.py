from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.database import Database
from app.core.config import get_config

settings = get_config()

client = AsyncIOMotorClient(settings.DATABASE_URL)
db: Database = client[settings.DATABASE_NAME]

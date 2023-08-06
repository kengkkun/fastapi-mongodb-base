from umongo.frameworks import MotorAsyncIOInstance
from app.core.config import settings
from motor.motor_asyncio import AsyncIOMotorClient

db = AsyncIOMotorClient(settings.MONGO_DATABASE_URI).main
instance = MotorAsyncIOInstance(db)

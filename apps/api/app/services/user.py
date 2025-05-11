from typing import Optional
from app.services.base import BaseService

class UserService(BaseService):
    def __init__(self):
        super().__init__()
        self.collection = self.db["users"]

    async def get_user_by_email(self, email: str) -> Optional[dict]:
        return await self.collection.find_one({"email": email})

    async def get_user_by_id(self, user_id: str) -> Optional[dict]:
        return await self.collection.find_one({"_id": user_id})

    async def create_user(self, user_data: dict) -> str:
        result = await self.collection.insert_one(user_data)
        return str(result.inserted_id)
    
    async def update_user(self, user_id: str, user_data: dict):
        return await self.collection.find_one_and_update(
            {"_id": user_id},
            {"$set": user_data},
            return_document=True  
        )
        
    async def delete_user(self, user_id: str):
        await self.collection.delete_one({"_id": user_id})
        
    async def update_user_by_email(self, email: str, user_data: dict):
        return await self.collection.find_one_and_update(
            {"email": email},
            {"$set": user_data},
            return_document=True  
        )

    async def isEmailUnique(self, email: str) -> bool:
        user = await self.get_user_by_email(email)
        return user is None
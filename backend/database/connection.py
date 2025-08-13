import os
from motor.motor_asyncio import AsyncIOMotorClient


client = AsyncIOMotorClient(os.getenv('MONGO_URL'))
database = client['recipe_db']

recipes_collection = database['recipes']
cuisines_collection = database['cuisines']
difficulty_collection = database['difficulty']
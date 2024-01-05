from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi

uri = "dburl"

client = AsyncIOMotorClient(uri, server_api=ServerApi('1'))

class MongoDB():
    async def insertTodayMostUsers(date,users):
        db = client.pconn
        await db[date].insert_one({date:users})

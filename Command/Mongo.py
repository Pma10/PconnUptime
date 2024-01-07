from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi

uri = "db"

client = AsyncIOMotorClient(uri, server_api=ServerApi('1'))

class MongoDB():
    def insertTodayMostUsers(date,users):
        db = client.pconn
        return db['users'].insert_one({date:users})
    def insertTodayMostPing(date,ping):
        db = client.pconn
        return db['ping'].insert_one({date:ping})

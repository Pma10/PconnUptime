from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.server_api import ServerApi

uri = "db"

client = AsyncIOMotorClient(uri, server_api=ServerApi('1'))

class MongoDB:
    @staticmethod
    async def update_max(data_type, date, max_value):
        db = client.pconn
        collection = db[data_type]

        existing_record = collection.find_one({'date': date})

        if existing_record:
            collection.update_one({'date': date}, {'$set': {data_type: max_value}})
        else:
            collection.insert_one({'date': date, data_type: max_value})

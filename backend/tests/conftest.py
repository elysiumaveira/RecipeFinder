import pytest
import mongomock
from motor.motor_asyncio import AsyncIOMotorClient


@pytest.fixture
async def mock_mongo():
    sync_client = mongomock.MongoClient()
    client = AsyncIOMotorClient(sync_client)
    db = client['test_db']
    yield db
    client.close()
    
    # db = client['test_db']
    # yield db
    # client.close()


# import pytest
# import asyncio
# from fastapi.testclient import TestClient
# from motor.motor_asyncio import AsyncIOMotorClient
# from unittest.mock import AsyncMock, MagicMock
# from backend.main import app


# @pytest.fixture(scope='session')
# def event_loop():
#     loop = asyncio.get_event_loop_policy().new_event_loop()
#     yield loop
#     loop.close()


# @pytest.fixture(scope='session')
# def test_client():
#     with TestClient(app) as client:
#         yield client
        

# @pytest.fixture(scope='function')
# async def mock_motor_client(monkeypatch):
#     mock_client = MagicMock()
#     mock_db = MagicMock()
#     mock_collection = AsyncMock()
    
#     mock_client.__getitem__.return_value = mock_db
#     mock_db.__getitem__.return_value = mock_collection



# @pytest.fixture(scope='session')
# def test_client():
#     with TestClient(app) as client:
#         yield client
        
        
# @pytest.fixture(scope='function')
# async def mock_motor_client(monkeypatch):
#     mock_client = AsyncMock(spec=AsyncIOMotorClient)
    
#     mock_db = AsyncMock()
#     mock_client.__getitem__.return_value = mock_db
    
#     mock_collection = AsyncMock()
#     mock_db.__getitem__.return_value = mock_collection
    
#     monkeypatch.setattr("backend.database.connection.client", mock_client)
#     monkeypatch.setattr("backend.database.connection.database", mock_db)
#     monkeypatch.setattr("backend.database.connection.difficulty_collection", mock_collection)

#     mock_collection.find_one.return_value = None  # Для проверки существующих записей
#     mock_collection.insert_one.return_value = AsyncMock(inserted_id="mock_id")
#     mock_collection.find_one.return_value = {"_id": "mock_id", "title": "НЕРЕАЛЬНО"}
    
#     yield mock_client



# TEST_DB_URL = 'mongodb://localhost:27017'
# TEST_DB_NAME = 'test_db'

# main_db = database
# main_client = client
# old_collections = {
#     'difficulty': difficulty_collection
# }


# @pytest.fixture(scope='session')
# def test_client():
#     with TestClient(app) as client:
#         yield client
        
        
# @pytest.fixture(scope='session')
# async def mongo_client():
#     client = AsyncIOMotorClient(TEST_DB_URL)
#     yield client
#     client.close()
        
        
# @pytest.fixture(scope='function')
# async def test_db(mongo_client):
#     test_db = mongo_client[TEST_DB_NAME]
#     yield test_db
#     await mongo_client.drop_database(TEST_DB_NAME)
    
    
# @pytest.fixture(scope='function')
# async def override_dependencies(test_db, monkeypatch):
#     monkeypatch.setattr("backend.database.connection.database", test_db)
#     monkeypatch.setattr("backend.database.connection.client", mongo_client)
#     monkeypatch.setattr("backend.database.connection.difficulty_collection", test_db["difficulty"])
    
    # monkeypatch.setattr("backend.database.connection.database", main_db)
    # monkeypatch.setattr("backend.database.connection.client", main_client)
    
    # for name, collection in old_collections.items():
    #     monkeypatch.setattr(f'backend.database.connection.{name}_collection', collection)
    
    # await mongo_client.drop_database(TEST_DB_NAME)

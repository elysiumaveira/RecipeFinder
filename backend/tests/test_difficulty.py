import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from backend.database.connection import difficulty_collection
from backend.difficulty.routes.difficulties import router
from backend.difficulty.schemas.difficutly import DifficultyCreate, DifficultyResponse


@pytest.fixture
def test_app(mock_mongo):
    app = FastAPI()
    app.include_router(router)
    
    app.dependency_overrides[difficulty_collection] = lambda: mock_mongo['difficulty']
    
    return app


@pytest.fixture
def client(test_app):
    return TestClient(test_app)


@pytest.mark.asyncio
async def test_create_difficulty(client, mock_mongo):
    test_data = {'title': 'Легчайшая'}
    
    response = client.post('/difficulty-create', json=test_data)
    
    assert response.status_code == 200
    assert response.json()['title'] == 'Легчайшая'


# def test_insert(mock_mongo):
#     collection = mock_mongo['test_collection']
#     collection.insert_one({'name': 'Alice'})
#     assert collection.find_one({'name': 'Alice'}) is not None


# @pytest.mark.asyncio
# async def test_create_difficulty(test_client, mock_motor_client):
#     item_data = {
#         'title': 'Нереально'
#     }

#     response = test_client.post('/difficulty-create', json=item_data)
#     assert response.status_code == 200


# @pytest.mark.asyncio
# async def test_create_difficulty(test_client, test_db):
#     item_data = {
#         'title': 'НЕРЕАЛЬНО',
#     }

#     response = test_client.post('/difficulty-create', json=item_data)
#     assert response.status_code == 200

#     diff_in_db = await test_db.difficulty.find_one({'title': 'НЕРЕАЛЬНО'})
#     assert diff_in_db is not None
#     assert diff_in_db['title'] == 'НЕРЕАЛЬНО'


# def test_smth():
#     assert 2 == 1+1
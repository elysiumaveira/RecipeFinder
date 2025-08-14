from typing import List
from fastapi import APIRouter, HTTPException
from bson import ObjectId
from backend.difficulty.schemas.difficutly import DifficultyCreate, DifficultyUpdate, DifficultyResponse
from backend.database.connection import difficulty_collection, database


router = APIRouter(tags=['Сложность'])


def difficulty_serializer(difficulty) -> dict:
    return {
        'id': str(difficulty['_id']),
        'title': difficulty['title'],
    }


@router.post('/difficulty-create', response_model=DifficultyResponse)
async def create_difficulty(difficulty: DifficultyCreate):
    existing = await difficulty_collection.find_one({'title': difficulty.title})
    if existing:
        raise HTTPException(status_code=400, detail='Уровень сложности уже существует')

    result = await difficulty_collection.insert_one(difficulty.model_dump())
    created = await difficulty_collection.find_one({'_id': result.inserted_id})

    return DifficultyResponse(**difficulty_serializer(created))


@router.get('/difficulties-list', response_model=List[DifficultyResponse])
async def get_all_difficulties():
    difficulties = await difficulty_collection.find().to_list(100)
    
    return [DifficultyResponse(**difficulty_serializer(d)) for d in difficulties]


@router.get('/difficulty/{id}', response_model=DifficultyResponse)
async def get_difficulty_by_id(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail='Неверный ID')
    
    difficulty = await difficulty_collection.find_one({'_id': ObjectId(id)})
    if not difficulty:
        raise HTTPException(status_code=404, detail='Уровень сложности не найден')
    
    return DifficultyResponse(**difficulty_serializer(difficulty))


@router.patch('/difficulty-edit/{id}', response_model=DifficultyResponse)
async def edit_difficulty(id: str, update_data: DifficultyUpdate):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail='Неверный ID')
    
    update_fields = {k: v for k, v in update_data.model_dump().items() if v is not None}
    
    await difficulty_collection.update_one(
        {'_id': ObjectId(id)},
        {'$set': update_fields}
    )
    
    updated = await difficulty_collection.find_one({'_id': ObjectId(id)})

    return DifficultyResponse(**difficulty_serializer(updated))


@router.delete('/difficulty-delete/{id}')
async def delete_difficulty(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail='Неверный ID')
    
    used = await database['recipes'].count_documents({'difficulty': ObjectId(id)})
    if used > 0:
        raise HTTPException(status_code=400, detail='Уровень используется в рецептах')
    
    await difficulty_collection.delete_one({'_id': ObjectId(id)})

    return {'message': 'Уровень сложности удален'}

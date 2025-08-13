from fastapi import APIRouter, HTTPException
from bson import ObjectId
from typing import List


from database.connection import cuisines_collection, database
from cuisine.schemas.cuisine import CuisineCreate, CuisineUpdate, CuisineResponse


router = APIRouter(tags=['Кухня'])


def cuisine_serializer(cuisine) -> dict:
    return {
        'id': str(cuisine['_id']),
        'title': cuisine['title'],
    }


@router.post('/cuisine-create', response_model=CuisineResponse)
async def create_cuisine(cuisine: CuisineCreate):
    existing = await cuisines_collection.find_one({'title': cuisine.title})
    if existing:
        raise HTTPException(status_code=400, detail='Вид кухни уже существует')
    
    result = await cuisines_collection.insert_one(cuisine.model_dump())
    created = await cuisines_collection.find_one({'_id': result.inserted_id})

    return CuisineResponse(**cuisine_serializer(created))


@router.get('/cuisines-list', response_model=List[CuisineResponse])
async def get_all_cuisines():
    cuisines = await cuisines_collection.find().to_list(100)

    return [CuisineResponse(**cuisine_serializer(c)) for c in cuisines]


@router.get('/cuisine/{id}', response_model=CuisineResponse)
async def get_cuisine_by_id(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail='Неверный ID')
    
    cuisine = await cuisines_collection.find_one({'_id': ObjectId(id)})
    if not cuisine:
        raise HTTPException(status_code=404, detail='Вид кухни не найден')
    
    return CuisineResponse(**cuisine_serializer(cuisine))


@router.patch('/cuisine-edit/{id}', response_model=CuisineResponse)
async def edit_cuisine(id: str, update_data: CuisineUpdate):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail='Неверный ID')
    
    update_fields = {k: v for k, v in update_data.model_dump().items() if v is not None}
    
    await cuisines_collection.update_one(
        {'_id': ObjectId(id)},
        {'$set': update_fields}
    )
    
    updated = await cuisines_collection.find_one({'_id': ObjectId(id)})
    return CuisineResponse(**cuisine_serializer(updated))


@router.delete('/cuisine-delete/{id}')
async def delete_cuisine(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(status_code=400, detail='Неверный ID')
    
    used = await database['recipes'].count_documents({'cuisine': ObjectId(id)})
    if used > 0:
        raise HTTPException(status_code=400, detail='Вид кухни используется в рецептах')
    
    await cuisines_collection.delete_one({'_id': ObjectId(id)})
    return {'message': 'Вид кухни удален'}

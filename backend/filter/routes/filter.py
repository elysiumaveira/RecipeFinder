from fastapi import Query, APIRouter, HTTPException
from typing import Optional, List
from bson import ObjectId

from backend.recipes.schemas.recipe import RecipeResponse
from backend.database.connection import recipes_collection


router = APIRouter(tags=['Фильтрация'])


def convert_objectid_to_str(obj):
    if isinstance(obj, dict):
        return {key: convert_objectid_to_str(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [convert_objectid_to_str(item) for item in obj]
    elif isinstance(obj, ObjectId):
        return str(obj)
    return obj


@router.get('/recipes/filter', response_model=List[RecipeResponse], status_code=200)
async def get_filtered_recipes_list(
    difficulty: Optional[str] = Query(None),
    cuisine: Optional[str] = Query(None),
    max_cooking_time: Optional[int] = None,
    min_cooking_time: Optional[int] = None,
    include_ingredients: Optional[List[str]] = Query(None),
    exclude_ingredients: Optional[List[str]] = Query(None),
):
    pipeline = []
    match_conditions = {}

    if difficulty:
        if not ObjectId(difficulty).is_valid:
            raise HTTPException(status_code=400, detail='Неверный формат ID')
        match_conditions['difficulty'] = ObjectId(difficulty)

    if cuisine:
        if not ObjectId(cuisine).is_valid:
            raise HTTPException(status_code=400, detail='Неверный формат ID')
        match_conditions['cuisine'] = ObjectId(cuisine)

    if min_cooking_time or max_cooking_time:
        match_conditions['cooking_time'] = {}
        if min_cooking_time:
            match_conditions['cooking_time']['$gte'] = min_cooking_time
        if max_cooking_time:
            match_conditions['cooking_time']['$lte'] = max_cooking_time

    if include_ingredients:
        pipeline.append({
            '$match': {
                'ingredients': {
                    '$not': {
                        '$elemMatch': {
                            '$nin': include_ingredients
                        }
                    }
                }
            }
        })

    if exclude_ingredients:
        pipeline.append({
            '$match': {
                'ingredients': {
                    '$nin': exclude_ingredients
                }
            }
        })

    if match_conditions:
        pipeline.append({'$match': match_conditions})

    pipeline.extend([
        {
            '$lookup': {
                'from': 'difficulty',
                'localField': 'difficulty',
                'foreignField': '_id',
                'as': 'difficulty',
            }
        },
        {
            '$lookup': {
                'from': 'cuisines',
                'localField': 'cuisine',
                'foreignField': '_id',
                'as': 'cuisine'
            }
        },
        {"$unwind": {"path": "$difficulty", "preserveNullAndEmptyArrays": True}},
        {"$unwind": {"path": "$cuisine", "preserveNullAndEmptyArrays": True}},
        {
            '$project': {
                '_id': {'$toString': '$_id'},
                'title': 1,
                'ingredients': 1,
                'preparation': 1,
                'cooking_time': 1,
                'difficulty': {
                    '_id': {'$toString': '$difficulty._id'},
                    'title': '$difficulty.title'
                },
                'cuisine': {
                    '_id': {'$toString': '$cuisine._id'},
                    'title': '$cuisine.title'
                }
            }
        }
    ])

    cursor = recipes_collection.aggregate(pipeline)
    result = await cursor.to_list(length=None)

    if not result:
        raise HTTPException(status_code=404, detail='Ничего не найдено')
    
    return convert_objectid_to_str(result)

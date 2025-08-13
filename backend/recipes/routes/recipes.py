from fastapi import APIRouter, HTTPException
from bson import ObjectId
from typing import List

from database.connection import recipes_collection, database
from recipes.schemas.recipe import RecipeCreate, RecipeUpdate, RecipeResponse


router = APIRouter(tags=['Рецепты'])


def convert_objectid_to_str(obj):
    if isinstance(obj, dict):
        return {key: convert_objectid_to_str(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [convert_objectid_to_str(item) for item in obj]
    elif isinstance(obj, ObjectId):
        return str(obj)
    return obj


def recipe_serializer(recipe) -> dict:
    return {
        'id': str(recipe['_id']),
        'title': recipe['title'],
        'ingredients': recipe['ingredients'],
        'preparation': recipe['preparation'],
        'cooking_time': recipe['cooking_time'],
        'difficulty': recipe['difficulty'],
        'cuisine': recipe['cuisine'],
    }


async def get_recipe_with_relations(recipe_id: str):
    if not ObjectId.is_valid(recipe_id):
        return None
    
    pipeline = [
        {"$match": {"_id": ObjectId(recipe_id)}},
        {
            "$lookup": {
                "from": "difficulty",
                "localField": "difficulty",
                "foreignField": "_id",
                "as": "difficulty"
            }
        },
        {
            "$lookup": {
                "from": "cuisines",
                "localField": "cuisine",
                "foreignField": "_id",
                "as": "cuisine"
            }
        },
        {"$unwind": {"path": "$difficulty", "preserveNullAndEmptyArrays": True}},
        {"$unwind": {"path": "$cuisine", "preserveNullAndEmptyArrays": True}},
        {
            "$project": {
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
                    'title': '$cuisine.title',
                },
            }
        }
    ]
    
    try:
        cursor = recipes_collection.aggregate(pipeline)
        result = await cursor.to_list(length=1)
        if result:
            return convert_objectid_to_str(result[0])
        return None
    except Exception as e:
        print(f"Ошибка при получении рецепта: {e}")
        return None


@router.post('/recipe-create', response_model=RecipeResponse, status_code=201)
async def create_recipe(recipe: RecipeCreate):
    try:
        difficulty_id = ObjectId(recipe.difficulty)
        cuisine_id = ObjectId(recipe.cuisine)
    except:
        raise HTTPException(status_code=400, detail='Неверный формат ID')

    difficulty = await database['difficulty'].find_one({'_id': difficulty_id})
    cuisine = await database['cuisines'].find_one({'_id': cuisine_id})

    if not difficulty:
        raise HTTPException(status_code=404, detail='Уровень сложности не задан')
    if not cuisine:
        raise HTTPException(status_code=404, detail='Кухня не указана')
    
    recipe_data = {
        'title': recipe.title,
        'ingredients': recipe.ingredients,
        'preparation': recipe.preparation,
        'cooking_time': recipe.cooking_time,
        'difficulty': difficulty_id,
        'cuisine': cuisine_id,
    }

    try:
        result = await recipes_collection.insert_one(recipe_data)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f'Ошибка сохранения: {str(e)}')

    try:
        pipeline = [
            {'$match': {'_id': result.inserted_id}},
            {
                '$lookup': {
                    'from': 'difficulty',
                    'localField': 'difficulty',
                    'foreignField': '_id',
                    'as': 'difficulty'
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
            {'$unwind': '$difficulty'},
            {'$unwind': '$cuisine'},
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
            },
        ]

        created_recipe = await recipes_collection.aggregate(pipeline).next()
    except Exception as e:
        return {
            'id': str(result.inserted_id),
            'title': recipe.title,
            'message': f'Рецепт создан, но возникла ошибка при получении полных данных ({str(e)})'
        }
    
    required_fields = [
        created_recipe.get('_id'),
        created_recipe.get('title'),
        created_recipe.get('difficulty', {}).get('_id'),
        created_recipe.get('difficulty', {}).get('title'),
        created_recipe.get('cuisine', {}).get('_id'),
        created_recipe.get('cuisine', {}).get('title')
    ]

    if not all(required_fields):
        raise HTTPException(status_code=400, detail='Неполные данные в запросе агрегации')

    return RecipeResponse(**created_recipe)


@router.get('/recipes-list', response_model=List[RecipeResponse])
async def get_all_recipes():
    recipes = []
    async for doc in recipes_collection.find():
        recipe = await get_recipe_with_relations(str(doc["_id"]))
        if recipe is not None:
            recipes.append(RecipeResponse(**recipe))

    return recipes


@router.get('/recipe-detail/{id}', response_model=RecipeResponse)
async def get_recipe(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(400, "Неверный ID рецепта")
    
    recipe = await get_recipe_with_relations(id)
    if not recipe:
        raise HTTPException(404, "Рецепт не найден")
    
    return RecipeResponse(**recipe)


@router.patch('/recipe-update/{id}', response_model=RecipeResponse)
async def update_recipe(id: str, update_data: RecipeUpdate):
    if not ObjectId.is_valid(id):
        raise HTTPException(400, "Неверный ID рецепта")
    
    
    current = await recipes_collection.find_one({"_id": ObjectId(id)})
    if not current:
        raise HTTPException(404, "Рецепт не найден")

    update_fields = {}
    
    if update_data.title:
        update_fields["title"] = update_data.title
    
    if update_data.ingredients:
        update_fields["ingredients"] = update_data.ingredients
    
    if update_data.preparation:
        update_fields["preparation"] = update_data.preparation
    
    if update_data.cooking_time:
        update_fields["cooking_time"] = update_data.cooking_time
    
    
    if update_data.difficulty:
        try:
            difficulty_id = ObjectId(update_data.difficulty)
            cuisine_id = ObjectId(update_data.cuisine)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f'Неверный формат ID: {str(e)}')

        difficulty = await database['difficulty'].find_one({"_id": difficulty_id})
        if not difficulty:
            raise HTTPException(404, "Уровень сложности не найден")
        update_fields["difficulty"] = difficulty["_id"]
    
    if update_data.cuisine:
        cuisine = await database['cuisines'].find_one({"_id": cuisine_id})
        if not cuisine:
            raise HTTPException(404, "Кухня не найдена")
        update_fields["cuisine"] = cuisine["_id"]
    
    
    if update_fields:
        await recipes_collection.update_one(
            {"_id": ObjectId(id)},
            {"$set": update_fields}
        )
    
    updated = await get_recipe_with_relations(id)

    return RecipeResponse(**updated)


@router.delete('/recipe-delete/{id}')
async def delete_recipe(id: str):
    if not ObjectId.is_valid(id):
        raise HTTPException(400, "Неверный ID рецепта")

    result = await recipes_collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(404, "Рецепт не найден")
    
    return {"message": "Рецепт успешно удален"}

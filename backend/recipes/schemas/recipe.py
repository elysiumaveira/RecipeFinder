from pydantic import BaseModel, ConfigDict, Field
from typing import List
from bson import ObjectId
from difficulty.schemas.difficutly import DifficultyResponse
from cuisine.schemas.cuisine import CuisineResponse


class RecipeCreate(BaseModel):
    title: str
    ingredients: List[str]
    preparation: str
    cooking_time: int
    difficulty: str
    cuisine: str


class RecipeUpdate(BaseModel):
    title: str | None = None
    ingredients: List[str] | None = None
    preparation: str | None = None
    cooking_time: int | None = None
    difficulty: str | None = None
    cuisine: str | None = None


class RecipeResponse(BaseModel):
    id: str = Field(alias="_id")
    title: str
    ingredients: List[str]
    preparation: str
    cooking_time: int
    difficulty: DifficultyResponse
    cuisine: CuisineResponse

    model_config = ConfigDict(
        populate_by_name=True,
        json_encoders={ObjectId: str},
        from_attributes = True,
        arbitrary_types_allowed = True,
    )
    
    # class Config:
    #     populate_by_name = True
    #     json_encoders = {ObjectId: str}
    #     from_attributes = True
    #     arbitrary_types_allowed = True

from pydantic import BaseModel, ConfigDict, Field
from bson import ObjectId


class DifficultyCreate(BaseModel):
    title: str


class DifficultyUpdate(BaseModel):
    title: str | None = None


class DifficultyResponse(BaseModel):
    id: str = Field(alias='_id')
    title: str

    model_config = ConfigDict(
        populate_by_name=True,
        json_encoders={ObjectId: str},
        from_attributes = True,
        arbitrary_types_allowed = True,
    )
    
    # class Config:
    #     populate_by_name = True
    #     json_encoders = {ObjectId: str}

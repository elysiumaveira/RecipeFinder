import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.recipes.routes.recipes import router as recipe_router
from backend.difficulty.routes.difficulties import router as difficulty_router
from backend.cuisine.routes.cuisines import router as cuisine_router
from backend.filter.routes.filter import router as filter_router


app = FastAPI(title='RecipeFinder API')

origins = os.getenv("CORS_ALLOWED_ORIGINS", "").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


app.include_router(recipe_router)
app.include_router(difficulty_router)
app.include_router(cuisine_router)
app.include_router(filter_router)


if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000)

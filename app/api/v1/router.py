from fastapi import APIRouter
from app.api.v1.views import city
from app.api.v1.views import genre


router = APIRouter()
router.include_router(city.router, prefix='/cities', tags=['cities'])
router.include_router(genre.router, prefix='/genres', tags=['genres'])

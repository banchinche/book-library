from fastapi import APIRouter
from app.api.v1.views import city


router = APIRouter()
router.include_router(city.router, prefix='/cities', tags=['cities'])

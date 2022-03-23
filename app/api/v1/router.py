from fastapi import APIRouter
from app.api.v1.views import author
from app.api.v1.views import book
from app.api.v1.views import city
from app.api.v1.views import genre
from app.api.v1.views import user


router = APIRouter()
router.include_router(author.router, prefix='/authors', tags=['authors'])
router.include_router(book.router, prefix='/books', tags=['books'])
router.include_router(city.router, prefix='/cities', tags=['cities'])
router.include_router(genre.router, prefix='/genres', tags=['genres'])
router.include_router(user.router, prefix='/users', tags=['users'])

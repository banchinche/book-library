from app.crud.base import DataAccessLayerBase
from app.models.book import Book
from app.schemas.book import BookCreate, BookUpdate


class BookCRUD(
    DataAccessLayerBase[Book, BookCreate, BookUpdate]
):
    ...


book = BookCRUD(Book)

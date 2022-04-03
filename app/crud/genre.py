from app.crud.base import DataAccessLayerBase
from app.models.genre import Genre
from app.schemas.genre import GenreCreate, GenreUpdate


class GenreCRUD(
    DataAccessLayerBase[Genre, GenreCreate, GenreUpdate]
):
    ...


genre = GenreCRUD(Genre)

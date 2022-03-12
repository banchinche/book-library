from app.crud.base import DataAccessLayerBase
from app.models.city import City
from app.schemas.city import CityCreate, CityUpdate


class CityCRUD(
    DataAccessLayerBase[City, CityCreate, CityUpdate]
):
    ...


city = CityCRUD(City)

from sqlalchemy import (
    Column,
    Date,
    Integer,
    ForeignKey,
    String,
)
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship


class PersonMixin:
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    birth_date = Column(Date)

    @declared_attr
    def city_id(self):
        return Column('city_id', ForeignKey('city.id'))

    @declared_attr
    def city(self):
        return relationship('City')

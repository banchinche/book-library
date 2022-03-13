from sqlalchemy import (
    Column,
    Date,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import relationship
from app.db.base_class import Base


class Person(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    birth_date = Column(Date)
    city_id = Column(Integer, ForeignKey('city.id'))

    # relationships
    authors = relationship(
        'Author',
        back_populates='person'
    )
    city = relationship(
        'City',
        back_populates='persons'
    )
    users = relationship(
        'User',
        back_populates='person'
    )

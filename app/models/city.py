from sqlalchemy import (
    Column,
    Integer,
    String,
)
from sqlalchemy.orm import relationship
from app.db.base_class import Base


class City(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False, index=True)

    # relationships
    persons = relationship(
        'Person',
        back_populates='city'
    )

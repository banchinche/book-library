from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
)
from sqlalchemy.orm import relationship
from app.db.base_class import Base


class Author(Base):
    id = Column(Integer, primary_key=True)
    person_id = Column(Integer, ForeignKey('person.id'))

    # relationships
    person = relationship(
        'Person',
        back_populates='authors'
    )

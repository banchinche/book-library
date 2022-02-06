from sqlalchemy import (
    Column,
    Integer,
    String,
)
from sqlalchemy.orm import relationship
from app.db.base_class import Base
from .book import book_genre


class Genre(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False, index=True)

    # relationships
    books = relationship(
        'Book',
        secondary=book_genre,
        back_populates='genres'
    )

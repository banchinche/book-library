from sqlalchemy import (
    Column,
    Date,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Table,
)
from sqlalchemy.orm import relationship
from app.db.base_class import Base
from .user import user_book

book_genre = Table(
    'book_genre',
    Base.metadata,
    Column('book_id', ForeignKey('book.id'), primary_key=True),
    Column('genre_id', ForeignKey('genre.id'), primary_key=True),
)


class Book(Base):
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False, index=True)
    release_date = Column(Date)
    price = Column(Numeric(precision=10, scale=2, asdecimal=True), nullable=True)
    author_id = Column(Integer, ForeignKey('author.id'))

    # relationships
    author = relationship(
        'Author',
        back_populates='books'
    )
    genres = relationship(
        'Genre',
        secondary=book_genre,
        back_populates='books'
    )
    users = relationship(
        'User',
        secondary=user_book,
        back_populates='books'
    )

from sqlalchemy import (
    Column,
    ForeignKey,
    String,
    Table,
)
from sqlalchemy.orm import relationship
from app.db.base_class import Base
from .mixins import PersonMixin


user_book = Table(
    'user_book',
    Base.metadata,
    Column('user_id', ForeignKey('user.id'), primary_key=True),
    Column('book_id', ForeignKey('book.id'), primary_key=True),
)


class User(PersonMixin, Base):
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String, nullable=False)

    # relationships
    books = relationship(
        'Book',
        secondary=user_book,
        back_populates='users'
    )

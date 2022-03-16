from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    Table,
)
from sqlalchemy.orm import relationship
from app.db.base_class import Base


user_book = Table(
    'user_book',
    Base.metadata,
    Column('user_id', ForeignKey('user.id'), primary_key=True),
    Column('book_id', ForeignKey('book.id'), primary_key=True),
)


class User(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String, nullable=False)
    person_id = Column(Integer, ForeignKey('person.id'))

    # relationships
    person = relationship(
        'Person',
        back_populates='user'
    )
    books = relationship(
        'Book',
        secondary=user_book,
        back_populates='users'
    )

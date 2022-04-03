from sqlalchemy.orm import relationship
from app.db.base_class import Base
from .mixins import PersonMixin


class Author(PersonMixin, Base):

    # relationships
    books = relationship(
        'Book',
        back_populates='author'
    )

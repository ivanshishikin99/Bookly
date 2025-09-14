from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.models import Base
from src.core.models.mixins import IdMixin, CreatedAtMixin, UpdatedAtMixin

if TYPE_CHECKING:
    from src.core.models.book import Book
    from src.core.models.book_genre_association_table import BookGenreAssociationTable


class Genre(Base, IdMixin, CreatedAtMixin, UpdatedAtMixin):
    name: Mapped[str] = mapped_column(nullable=False)
    books: Mapped[list["Book"]] = relationship(secondary="BookGenreAssociationTable", back_populates="genres", lazy="selectin")
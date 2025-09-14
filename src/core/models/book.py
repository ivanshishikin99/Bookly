from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.models import Base
from src.core.models.mixins import IdMixin, CreatedAtMixin, UpdatedAtMixin

if TYPE_CHECKING:
    from src.core.models.author import Author
    from src.core.models.review import Review
    from src.core.models.genre import Genre
    from src.core.models.book_genre_association_table import BookGenreAssociationTable


class Book(Base, IdMixin, CreatedAtMixin, UpdatedAtMixin):
    title: Mapped[str] = mapped_column(nullable=False, index=True)
    year_of_release: Mapped[int] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    author: Mapped["Author"] = relationship(back_populates="books", lazy="selectin")
    author_id: Mapped[int] = mapped_column(ForeignKey("author.id"), index=True)
    reviews: Mapped[list["Review"]] = relationship(back_populates="book", cascade="all, delete", lazy="selectin")
    genres: Mapped[list["Genre"]] = relationship(secondary="BookGenreAssociationTable", back_populates="books", lazy="selectin")
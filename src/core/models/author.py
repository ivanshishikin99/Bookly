from datetime import date

from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.models import Base
from src.core.models.mixins import IdMixin, CreatedAtMixin, UpdatedAtMixin

if TYPE_CHECKING:
    from src.core.models.book import Book


class Author(Base, IdMixin, CreatedAtMixin, UpdatedAtMixin):
    full_name: Mapped[str] = mapped_column(nullable=False)
    date_of_birth: Mapped[date] = mapped_column(nullable=False)
    date_of_death: Mapped[date] = mapped_column(nullable=True)
    bio: Mapped[str] = mapped_column(nullable=True)
    books: Mapped[list["Book"]] = relationship(back_populates="author", cascade="all, delete")
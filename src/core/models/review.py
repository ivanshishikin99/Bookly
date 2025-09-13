from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.models import Base
from src.core.models.mixins import IdMixin, CreatedAtMixin, UpdatedAtMixin

if TYPE_CHECKING:
    from src.core.models.book import Book
    from src.core.models.user import User


class Review(Base, IdMixin, CreatedAtMixin, UpdatedAtMixin):
    title: Mapped[str] = mapped_column(nullable=False)
    text: Mapped[str] = mapped_column(nullable=False)
    book: Mapped["Book"] = relationship(back_populates="reviews", lazy="selectin")
    book_id: Mapped[int] = mapped_column(ForeignKey("book.id"), index=True)
    user: Mapped["User"] = relationship(back_populates="reviews", lazy="selectin")
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), index=True)
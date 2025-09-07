from sqlalchemy.orm import Mapped, mapped_column

from src.core.models import Base
from src.core.models.mixins import IdMixin, CreatedAtMixin, UpdatedAtMixin


class Book(Base, IdMixin, CreatedAtMixin, UpdatedAtMixin):
    title: Mapped[str] = mapped_column(nullable=False, index=True)
    year_of_release: Mapped[int] = mapped_column(nullable=False)
    author: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
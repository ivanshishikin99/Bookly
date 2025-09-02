from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.models import Base
from src.core.models.mixins import IdMixin, CreatedAtMixin, UpdatedAtMixin

if TYPE_CHECKING:
    from src.core.models.user import User


class Profile(Base, IdMixin, CreatedAtMixin, UpdatedAtMixin):
    first_name: Mapped[str] = mapped_column(nullable=True)
    last_name: Mapped[str] = mapped_column(nullable=True)
    country: Mapped[str] = mapped_column(nullable=True)
    bio: Mapped[str] = mapped_column(nullable=True)
    sex: Mapped[str] = mapped_column(nullable=True)
    date_of_birth: Mapped[datetime] = mapped_column(nullable=True)
    is_public: Mapped[bool] = mapped_column(nullable=False, default=True)
    user: Mapped["User"] = relationship(back_populates="profile")
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), unique=True)
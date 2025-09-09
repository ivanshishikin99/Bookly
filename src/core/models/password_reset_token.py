from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.core.models import Base
from src.core.models.mixins import IdMixin, CreatedAtMixin


class PasswordResetToken(Base, IdMixin, CreatedAtMixin):
    token: Mapped[UUID] = mapped_column(nullable=False)
    user_email: Mapped[str] = mapped_column(ForeignKey("user.email"), unique=True)
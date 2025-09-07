from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.core.models import Base
from src.core.models.mixins import IdMixin, CreatedAtMixin


class EmailVerificationToken(Base, IdMixin, CreatedAtMixin):
    token: Mapped[UUID]
    user_email: Mapped[str] = mapped_column(ForeignKey("user.email"), unique=True)

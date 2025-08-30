from sqlalchemy.orm import Mapped, mapped_column

from src.core.models import Base
from src.core.models.mixins import IdMixin, CreatedAtMixin, UpdatedAtMixin


class User(Base, IdMixin, CreatedAtMixin, UpdatedAtMixin):
    username: Mapped[str] = mapped_column(nullable=False, unique=True, index=True)
    password: Mapped[bytes] = mapped_column(nullable=False)
    verified: Mapped[bool] = mapped_column(nullable=False)
    role_access: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
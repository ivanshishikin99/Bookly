from sqlalchemy.orm import Mapped, mapped_column

from src.core.models import Base
from src.core.models.mixins import IdMixin, CreatedAtMixin, UpdatedAtMixin


class SuperUser(Base, IdMixin, CreatedAtMixin, UpdatedAtMixin):
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[bytes] = mapped_column(nullable=False)
    role_access: Mapped[str] = mapped_column(default="Super user", server_default="Super user")
    verified: Mapped[bool] = mapped_column(default=True)
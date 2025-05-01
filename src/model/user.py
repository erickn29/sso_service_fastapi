from sqlalchemy import TIMESTAMP, String, Text, func, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from model.base import Base


class User(Base):
    __tablename__ = "user"

    password: Mapped[str] = mapped_column(Text)
    email: Mapped[str] = mapped_column(String(320))
    first_name: Mapped[str] = mapped_column(String(16), default="")
    last_name: Mapped[str] = mapped_column(String(16), default="")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
    is_service: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.current_timestamp(),
        nullable=False,
    )
    updated_at = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.current_timestamp(),
        nullable=False,
        onupdate=func.current_timestamp(),
    )

    @property
    def full_name(self) -> str:
        first_name = self.first_name or "User"
        last_name = self.last_name or str(self.id)[:5]
        return first_name + " " + last_name

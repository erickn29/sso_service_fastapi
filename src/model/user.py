from sqlalchemy import TIMESTAMP, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from model.base import Base


class User(Base):
    password: Mapped[str] = mapped_column(Text)
    email: Mapped[str] = mapped_column(String(320))
    first_name: Mapped[str] = mapped_column(String(16), default="")
    last_name: Mapped[str] = mapped_column(String(16), default="")
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

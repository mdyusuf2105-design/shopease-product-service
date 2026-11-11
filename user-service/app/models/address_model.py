from datetime import datetime, timezone

from sqlalchemy import (
    Integer, String, Boolean, DateTime, ForeignKey
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.connection import Base


class UserAddress(Base):
    __tablename__ = "user_addresses"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("user_profiles.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )

    address_type: Mapped[str] = mapped_column(
        String(30), default="Home", nullable=False
    )

    full_name: Mapped[str] = mapped_column(
        String(150), nullable=False
    )

    phone_number: Mapped[str] = mapped_column(
        String(20), nullable=False
    )

    address_line_1: Mapped[str] = mapped_column(
        String(255), nullable=False
    )

    address_line_2: Mapped[str | None] = mapped_column(
        String(255), nullable=True
    )

    city: Mapped[str] = mapped_column(
        String(100), nullable=False
    )

    state: Mapped[str] = mapped_column(
        String(100), nullable=False
    )

    country: Mapped[str] = mapped_column(
        String(100), nullable=False
    )

    postal_code: Mapped[str] = mapped_column(
        String(20), nullable=False
    )

    is_default: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    user = relationship(
        "UserProfile",
        back_populates="addresses"
    )

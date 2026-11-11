from datetime import datetime, timezone

from sqlalchemy import (
    String, Integer, Date, DateTime, UniqueConstraint
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.connection import Base


class UserProfile(Base):
    __tablename__ = "user_profiles"

    __table_args__ = (
        UniqueConstraint("auth_user_id", name="uq_user_profiles_auth_user_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    auth_user_id: Mapped[int] = mapped_column(
        Integer, nullable=False, index=True
    )

    full_name: Mapped[str] = mapped_column(
        String(150), nullable=False
    )

    phone_number: Mapped[str | None] = mapped_column(
        String(20), nullable=True
    )

    date_of_birth: Mapped[Date | None] = mapped_column(
        Date, nullable=True
    )

    gender: Mapped[str | None] = mapped_column(
        String(30), nullable=True
    )

    profile_image: Mapped[str | None] = mapped_column(
        String(500), nullable=True
    )

    is_active: Mapped[bool] = mapped_column(
        default=True, nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    addresses = relationship(
        "UserAddress",
        back_populates="user",
        cascade="all, delete-orphan"
    )

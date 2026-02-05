"""Customer model."""

import uuid
from datetime import datetime

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if False:  # TYPE_CHECKING alternative for runtime
    from app.models.booking import Booking


class Customer(Base):
    """Customer model representing a person who can rent cars."""

    __tablename__ = "customers"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    phone: Mapped[str] = mapped_column(String(20), nullable=False)
    driver_license: Mapped[str] = mapped_column(String(50), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )

    bookings: Mapped[list["Booking"]] = relationship(back_populates="customer")

    def __repr__(self) -> str:
        return f"<Customer {self.first_name} {self.last_name} ({self.email})>"

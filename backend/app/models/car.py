"""Car model."""

import enum
import uuid
from datetime import datetime

from sqlalchemy import DateTime, Enum, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base

if False:  # TYPE_CHECKING alternative for runtime
    from app.models.booking import Booking


class CarCategory(str, enum.Enum):
    """Car category enumeration."""

    ECONOMY = "economy"
    STANDARD = "standard"
    LUXURY = "luxury"
    SUV = "suv"


class CarStatus(str, enum.Enum):
    """Car status enumeration."""

    AVAILABLE = "available"
    RENTED = "rented"
    MAINTENANCE = "maintenance"


class Car(Base):
    """Car model representing a vehicle in the rental fleet."""

    __tablename__ = "cars"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    make: Mapped[str] = mapped_column(String(100), nullable=False)
    model: Mapped[str] = mapped_column(String(100), nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    license_plate: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    daily_rate: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    category: Mapped[CarCategory] = mapped_column(
        Enum(CarCategory), default=CarCategory.STANDARD
    )
    status: Mapped[CarStatus] = mapped_column(
        Enum(CarStatus), default=CarStatus.AVAILABLE
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, nullable=False
    )

    bookings: Mapped[list["Booking"]] = relationship(back_populates="car")

    def __repr__(self) -> str:
        return f"<Car {self.make} {self.model} ({self.license_plate})>"

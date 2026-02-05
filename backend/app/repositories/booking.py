"""Booking repository for data access."""

from datetime import date

from sqlalchemy import and_, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.booking import Booking, BookingStatus
from app.repositories.base import BaseRepository


class BookingRepository(BaseRepository[Booking]):
    """Repository for Booking model operations."""

    def __init__(self, session: AsyncSession):
        super().__init__(Booking, session)

    async def get_by_car_id(self, car_id: str) -> list[Booking]:
        """Get all bookings for a specific car."""
        result = await self.session.execute(
            select(Booking).where(Booking.car_id == car_id)
        )
        return list(result.scalars().all())

    async def get_by_customer_id(self, customer_id: str) -> list[Booking]:
        """Get all bookings for a specific customer."""
        result = await self.session.execute(
            select(Booking).where(Booking.customer_id == customer_id)
        )
        return list(result.scalars().all())

    async def get_overlapping_bookings(
        self,
        car_id: str,
        start_date: date,
        end_date: date,
        exclude_booking_id: str | None = None,
    ) -> list[Booking]:
        """Get bookings that overlap with the given date range for a car."""
        query = select(Booking).where(
            and_(
                Booking.car_id == car_id,
                Booking.status.in_([BookingStatus.RESERVED, BookingStatus.ACTIVE]),
                or_(
                    and_(
                        Booking.start_date <= start_date,
                        Booking.end_date >= start_date,
                    ),
                    and_(
                        Booking.start_date <= end_date,
                        Booking.end_date >= end_date,
                    ),
                    and_(
                        Booking.start_date >= start_date,
                        Booking.end_date <= end_date,
                    ),
                ),
            )
        )

        if exclude_booking_id:
            query = query.where(Booking.id != exclude_booking_id)

        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def get_filtered(
        self,
        status: BookingStatus | None = None,
        car_id: str | None = None,
        customer_id: str | None = None,
    ) -> list[Booking]:
        """Get bookings with optional filters."""
        query = select(Booking)

        if status is not None:
            query = query.where(Booking.status == status)
        if car_id is not None:
            query = query.where(Booking.car_id == car_id)
        if customer_id is not None:
            query = query.where(Booking.customer_id == customer_id)

        result = await self.session.execute(query)
        return list(result.scalars().all())

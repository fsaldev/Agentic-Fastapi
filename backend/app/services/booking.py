"""Booking service for business logic."""

from datetime import date

from app.models.booking import Booking, BookingStatus
from app.models.car import CarStatus
from app.repositories.booking import BookingRepository
from app.repositories.car import CarRepository
from app.repositories.customer import CustomerRepository
from app.schemas.booking import BookingCreate


class BookingService:
    """Service for booking-related business logic."""

    def __init__(
        self,
        booking_repository: BookingRepository,
        car_repository: CarRepository,
        customer_repository: CustomerRepository,
    ):
        self.booking_repository = booking_repository
        self.car_repository = car_repository
        self.customer_repository = customer_repository

    async def get_booking(self, booking_id: str) -> Booking | None:
        """Get a booking by ID."""
        return await self.booking_repository.get_by_id(booking_id)

    async def get_bookings(
        self,
        status: BookingStatus | None = None,
        car_id: str | None = None,
        customer_id: str | None = None,
    ) -> list[Booking]:
        """Get all bookings with optional filters."""
        return await self.booking_repository.get_filtered(
            status=status, car_id=car_id, customer_id=customer_id
        )

    async def create_booking(self, data: BookingCreate) -> Booking:
        """Create a new booking (reservation)."""
        car = await self.car_repository.get_by_id(data.car_id)
        if not car:
            raise ValueError(f"Car with ID '{data.car_id}' not found")
        if car.status == CarStatus.MAINTENANCE:
            raise ValueError("Car is currently under maintenance")

        customer = await self.customer_repository.get_by_id(data.customer_id)
        if not customer:
            raise ValueError(f"Customer with ID '{data.customer_id}' not found")

        if data.start_date >= data.end_date:
            raise ValueError("Start date must be before end date")
        if data.start_date < date.today():
            raise ValueError("Start date cannot be in the past")

        overlapping = await self.booking_repository.get_overlapping_bookings(
            car_id=data.car_id,
            start_date=data.start_date,
            end_date=data.end_date,
        )
        if overlapping:
            raise ValueError("Car is not available for the selected dates")

        days = (data.end_date - data.start_date).days
        total_cost = float(car.daily_rate) * days

        booking = Booking(
            car_id=data.car_id,
            customer_id=data.customer_id,
            start_date=data.start_date,
            end_date=data.end_date,
            total_cost=total_cost,
            status=BookingStatus.RESERVED,
        )
        return await self.booking_repository.create(booking)

    async def pickup_car(self, booking_id: str) -> Booking | None:
        """Start a rental (reserved -> active)."""
        booking = await self.booking_repository.get_by_id(booking_id)
        if not booking:
            return None
        if booking.status != BookingStatus.RESERVED:
            raise ValueError("Only reserved bookings can be picked up")

        car = await self.car_repository.get_by_id(booking.car_id)
        if car:
            car.status = CarStatus.RENTED
            await self.car_repository.update(car)

        booking.status = BookingStatus.ACTIVE
        return await self.booking_repository.update(booking)

    async def return_car(self, booking_id: str) -> Booking | None:
        """Complete a rental (active -> completed)."""
        booking = await self.booking_repository.get_by_id(booking_id)
        if not booking:
            return None
        if booking.status != BookingStatus.ACTIVE:
            raise ValueError("Only active bookings can be returned")

        car = await self.car_repository.get_by_id(booking.car_id)
        if car:
            car.status = CarStatus.AVAILABLE
            await self.car_repository.update(car)

        booking.status = BookingStatus.COMPLETED
        booking.actual_return_date = date.today()
        return await self.booking_repository.update(booking)

    async def cancel_booking(self, booking_id: str) -> Booking | None:
        """Cancel a booking."""
        booking = await self.booking_repository.get_by_id(booking_id)
        if not booking:
            return None
        if booking.status not in [BookingStatus.RESERVED, BookingStatus.ACTIVE]:
            raise ValueError("Only reserved or active bookings can be cancelled")

        if booking.status == BookingStatus.ACTIVE:
            car = await self.car_repository.get_by_id(booking.car_id)
            if car:
                car.status = CarStatus.AVAILABLE
                await self.car_repository.update(car)

        booking.status = BookingStatus.CANCELLED
        return await self.booking_repository.update(booking)

    async def check_availability(
        self, car_id: str, start_date: date, end_date: date
    ) -> dict:
        """Check if a car is available for a date range."""
        car = await self.car_repository.get_by_id(car_id)
        if not car:
            raise ValueError(f"Car with ID '{car_id}' not found")

        overlapping = await self.booking_repository.get_overlapping_bookings(
            car_id=car_id,
            start_date=start_date,
            end_date=end_date,
        )

        if overlapping:
            conflicts = [
                {
                    "booking_id": b.id,
                    "start_date": b.start_date.isoformat(),
                    "end_date": b.end_date.isoformat(),
                }
                for b in overlapping
            ]
            return {"available": False, "conflicts": conflicts}

        return {"available": True, "conflicts": []}

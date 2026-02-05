"""Car service for business logic."""

from app.models.car import Car, CarCategory, CarStatus
from app.repositories.car import CarRepository
from app.schemas.car import CarCreate, CarUpdate


class CarService:
    """Service for car-related business logic."""

    def __init__(self, repository: CarRepository):
        self.repository = repository

    async def get_car(self, car_id: str) -> Car | None:
        """Get a car by ID."""
        return await self.repository.get_by_id(car_id)

    async def get_cars(
        self,
        status: CarStatus | None = None,
        category: CarCategory | None = None,
    ) -> list[Car]:
        """Get all cars with optional filters."""
        return await self.repository.get_filtered(status=status, category=category)

    async def create_car(self, data: CarCreate) -> Car:
        """Create a new car."""
        existing = await self.repository.get_by_license_plate(data.license_plate)
        if existing:
            raise ValueError(
                f"Car with license plate '{data.license_plate}' already exists"
            )

        car = Car(
            make=data.make,
            model=data.model,
            year=data.year,
            license_plate=data.license_plate,
            daily_rate=data.daily_rate,
            category=data.category,
        )
        return await self.repository.create(car)

    async def update_car(self, car_id: str, data: CarUpdate) -> Car | None:
        """Update an existing car."""
        car = await self.repository.get_by_id(car_id)
        if not car:
            return None

        if data.license_plate and data.license_plate != car.license_plate:
            existing = await self.repository.get_by_license_plate(data.license_plate)
            if existing:
                raise ValueError(
                    f"Car with license plate '{data.license_plate}' already exists"
                )

        update_data = data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(car, field, value)

        return await self.repository.update(car)

    async def delete_car(self, car_id: str) -> bool:
        """Delete a car."""
        car = await self.repository.get_by_id(car_id)
        if not car:
            return False
        await self.repository.delete(car)
        return True

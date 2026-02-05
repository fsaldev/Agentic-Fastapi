"""Car repository for data access."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.car import Car, CarCategory, CarStatus
from app.repositories.base import BaseRepository


class CarRepository(BaseRepository[Car]):
    """Repository for Car model operations."""

    def __init__(self, session: AsyncSession):
        super().__init__(Car, session)

    async def get_by_license_plate(self, license_plate: str) -> Car | None:
        """Get a car by its license plate."""
        result = await self.session.execute(
            select(Car).where(Car.license_plate == license_plate)
        )
        return result.scalar_one_or_none()

    async def get_filtered(
        self,
        status: CarStatus | None = None,
        category: CarCategory | None = None,
    ) -> list[Car]:
        """Get cars with optional filters."""
        query = select(Car)

        if status is not None:
            query = query.where(Car.status == status)
        if category is not None:
            query = query.where(Car.category == category)

        result = await self.session.execute(query)
        return list(result.scalars().all())

"""Customer service for business logic."""

from app.models.customer import Customer
from app.repositories.customer import CustomerRepository
from app.schemas.customer import CustomerCreate, CustomerUpdate


class CustomerService:
    """Service for customer-related business logic."""

    def __init__(self, repository: CustomerRepository):
        self.repository = repository

    async def get_customer(self, customer_id: str) -> Customer | None:
        """Get a customer by ID."""
        return await self.repository.get_by_id(customer_id)

    async def get_customers(self) -> list[Customer]:
        """Get all customers."""
        return await self.repository.get_all()

    async def create_customer(self, data: CustomerCreate) -> Customer:
        """Create a new customer."""
        existing = await self.repository.get_by_email(data.email)
        if existing:
            raise ValueError(f"Customer with email '{data.email}' already exists")

        customer = Customer(
            first_name=data.first_name,
            last_name=data.last_name,
            email=data.email,
            phone=data.phone,
            driver_license=data.driver_license,
        )
        return await self.repository.create(customer)

    async def update_customer(
        self, customer_id: str, data: CustomerUpdate
    ) -> Customer | None:
        """Update an existing customer."""
        customer = await self.repository.get_by_id(customer_id)
        if not customer:
            return None

        if data.email and data.email != customer.email:
            existing = await self.repository.get_by_email(data.email)
            if existing:
                raise ValueError(f"Customer with email '{data.email}' already exists")

        update_data = data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(customer, field, value)

        return await self.repository.update(customer)

    async def delete_customer(self, customer_id: str) -> bool:
        """Delete a customer."""
        customer = await self.repository.get_by_id(customer_id)
        if not customer:
            return False
        await self.repository.delete(customer)
        return True

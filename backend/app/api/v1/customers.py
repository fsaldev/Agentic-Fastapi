"""Customer API endpoints."""

from fastapi import APIRouter, HTTPException

from app.api.dependencies import CustomerServiceDep
from app.schemas.customer import CustomerCreate, CustomerResponse, CustomerUpdate

router = APIRouter()


@router.get("", response_model=list[CustomerResponse])
async def list_customers(service: CustomerServiceDep):
    """List all customers."""
    return await service.get_customers()


@router.get("/{customer_id}", response_model=CustomerResponse)
async def get_customer(customer_id: str, service: CustomerServiceDep):
    """Get a customer by ID."""
    customer = await service.get_customer(customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer


@router.post("", response_model=CustomerResponse, status_code=201)
async def create_customer(data: CustomerCreate, service: CustomerServiceDep):
    """Create a new customer."""
    return await service.create_customer(data)


@router.put("/{customer_id}", response_model=CustomerResponse)
async def update_customer(
    customer_id: str, data: CustomerUpdate, service: CustomerServiceDep
):
    """Update a customer."""
    customer = await service.update_customer(customer_id, data)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer


@router.delete("/{customer_id}", status_code=204)
async def delete_customer(customer_id: str, service: CustomerServiceDep):
    """Delete a customer."""
    deleted = await service.delete_customer(customer_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Customer not found")

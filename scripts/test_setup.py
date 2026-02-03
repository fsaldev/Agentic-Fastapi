"""Test script to verify project setup."""

import asyncio

from app.main import app
from app.database import engine
from app.models import Base


async def test():
    """Test database creation and app configuration."""
    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Database tables created successfully")

    # Test app configuration
    print(f"App title: {app.title}")
    print(f"Routes: {len(app.routes)} routes registered")

    # List routes
    for route in app.routes:
        if hasattr(route, "path") and hasattr(route, "methods"):
            print(f"  {route.methods} {route.path}")


if __name__ == "__main__":
    asyncio.run(test())

"""FastAPI application entry point."""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.v1.router import router as api_v1_router
from app.config import settings
from app.database import engine
from app.exceptions.handlers import register_exception_handlers
from app.models import Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler for startup/shutdown events."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


app = FastAPI(
    title=settings.app_name,
    description="RESTful backend API for managing a car rental business",
    version="1.0.0",
    lifespan=lifespan,
)

register_exception_handlers(app)

app.include_router(api_v1_router)


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}

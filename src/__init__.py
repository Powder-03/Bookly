from fastapi import FastAPI
from src.books.routes import book_router
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize resources here if needed
    print(f"Server is starting")
    yield
    print(f"Server is shutting down")
    # Cleanup resources here if needed

version = "v1"

app = FastAPI(
    title="Bookly API",
    description="A FastAPI application for managing books",
    version=version,
    docs_url="/docs",
    redoc_url="/redoc"
)

app.include_router(book_router, prefix=f"/api/{version}/books", tags=["books"])



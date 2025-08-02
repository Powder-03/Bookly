from fastapi import FastAPI
from src.books.routes import book_router
from src.auth.routes import auth_router
from contextlib import asynccontextmanager
from src.db.main import init_db

@asynccontextmanager
async def life_span(app: FastAPI):
    # Initialize resources here if needed
    print(f"Server is starting")
    await init_db()
    yield
    print(f"Server is shutting down")
    # Cleanup resources here if needed

version = "v1"

app = FastAPI(
    title="Bookly API",
    description="A FastAPI application for managing books",
    version=version,
    lifespan=life_span,
    docs_url="/docs",
    redoc_url="/redoc"
)

app.include_router(book_router, prefix=f"/api/{version}/books", tags=["books"])
app.include_router(auth_router, prefix=f"/api/{version}/auth", tags=["auth"])



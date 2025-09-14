from fastapi import FastAPI
from src.books.routes import book_router
from src.auth.routes import auth_router
from src.tags.routes import tags_router  
from src.reviews.routes import review_router  
from src.errors import register_all_errors  
from src.middleware import register_middleware  

version = "v1"

app = FastAPI(
    title="Bookly API",
    description="A FastAPI application for managing books",
    version=version,
    docs_url="/docs",
    redoc_url="/redoc"
)

app.include_router(book_router, prefix=f"/api/{version}/books", tags=["books"])
app.include_router(auth_router, prefix=f"/api/{version}/auth", tags=["auth"])
app.include_router(tags_router, prefix=f"/api/{version}/tags", tags=["tags"]) 
app.include_router(review_router, prefix=f"/api/{version}/reviews", tags=["reviews"])  

# Register error handlers and middleware
register_all_errors(app)  
register_middleware(app)  
from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class BookCreateModel(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    author: str = Field(..., min_length=1, max_length=100)
    publisher: str = Field(..., min_length=1, max_length=100)
    published_date: str = Field(..., description="Date in YYYY-MM-DD format")
    pagecount: int = Field(..., gt=0, description="Number of pages must be positive")
    language: str = Field(..., min_length=1, max_length=50)

class Book(BaseModel):
    id: int
    title: str
    author: str
    publisher: str
    published_date: str
    page_count: int
    language: str
    
class BookUpdateModel(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    author: Optional[str] = Field(None, min_length=1, max_length=100)
    publisher: Optional[str] = Field(None, min_length=1, max_length=100)
    published_date: Optional[str] = Field(None, description="Date in YYYY-MM-DD format")
    pagecount: Optional[int] = Field(None, gt=0, description="Number of pages must be positive")
    language: Optional[str] = Field(None, min_length=1, max_length=50)
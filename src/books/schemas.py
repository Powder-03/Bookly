import uuid
from datetime import date, datetime
from typing import List

from pydantic import BaseModel, Field

from src.reviews.schemas import ReviewModel
from src.tags.schemas import TagModel


class Book(BaseModel):
    uid: uuid.UUID = Field(default_factory=uuid.uuid4)
    title: str
    author: str
    publisher: str
    published_date: date
    page_count: int
    language: str
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class BookDetailModel(Book):
    reviews: List[ReviewModel]
    tags: List[TagModel]


class BookCreateModel(BaseModel):
    title: str
    author: str
    publisher: str
    published_date: str
    page_count: int
    language: str


class BookUpdateModel(BaseModel):
    title: str
    author: str
    publisher: str
    page_count: int
    language: str
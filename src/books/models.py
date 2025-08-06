from sqlmodel import SQLModel , Field , Column
from datetime import datetime, date
import uuid 
import sqlalchemy.dialects.postgresql as pg
from typing import Optional

class Book(SQLModel, table=True):
    
    __tablename__ = "books"
    
    
    uid: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False
        )
    )
    title: str
    author: str
    publisher: str
    published_date: date
    page_count: int
    language: str
    user_uid: Optional[uuid.UUID] = Field(default=None, foreign_key="users.uid", nullable=True)  # Optional user association
    # Note: user_uid is optional, allowing books to exist without a user association
    # If you want to enforce that every book must have a user, you can remove the `Optional` and `nullable=True` attributes.
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP(timezone=True), nullable=False), default_factory=datetime.now) #its an sqlalchemy column not an pydantic column
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP(timezone=True), nullable=False), default_factory=datetime.now)


    def __repr__(self):
        return f"<Book {self.title}>"
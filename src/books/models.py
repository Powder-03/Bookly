from sqlmodel import SQLModel , Field , Column
from datetime import datetime
import uuid 
import sqlalchemy.dialects.postgresql as pg

class Book(SQLModel, table=True):
    uid: uuid.UUID = Field(
        sa_column=Column(
            pg.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False
        )
    )
    title: str
    author: str
    publisher: str
    published_date: str
    page_count: int
    language: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

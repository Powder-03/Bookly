import uuid
from datetime import date, datetime
from typing import List, Optional

from sqlalchemy import Column, ForeignKey, String, Table, func
from sqlalchemy.dialects.postgresql import UUID, VARCHAR, TIMESTAMP
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


book_tag = Table(
    "book_tag",
    Base.metadata,
    Column("book_id", UUID(as_uuid=True), ForeignKey("books.uid"), primary_key=True),
    Column("tag_id", UUID(as_uuid=True), ForeignKey("tags.uid"), primary_key=True),
)


class User(Base):
    __tablename__ = "users"

    uid: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    username: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String)
    first_name: Mapped[str] = mapped_column(String)
    last_name: Mapped[str] = mapped_column(String)
    role: Mapped[str] = mapped_column(VARCHAR, server_default="user")
    is_verified: Mapped[bool] = mapped_column(default=False)
    password_hash: Mapped[str] = mapped_column(VARCHAR)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.now)

    books: Mapped[List["Book"]] = relationship(
        back_populates="user", lazy="selectin"
    )
    reviews: Mapped[List["Review"]] = relationship(
        back_populates="user", lazy="selectin"
    )

    def __repr__(self):
        return f"<User {self.username}>"


class Tag(Base):
    __tablename__ = "tags"

    uid: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(VARCHAR, nullable=False)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.now)

    books: Mapped[List["Book"]] = relationship(
        secondary=book_tag, back_populates="tags", lazy="selectin"
    )

    def __repr__(self) -> str:
        return f"<Tag {self.name}>"


class Book(Base):
    __tablename__ = "books"

    uid: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    title: Mapped[str] = mapped_column(String)
    author: Mapped[str] = mapped_column(String)
    publisher: Mapped[str] = mapped_column(String)
    published_date: Mapped[date] = mapped_column()
    page_count: Mapped[int] = mapped_column()
    language: Mapped[str] = mapped_column(String)
    user_uid: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.uid"), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.now)

    user: Mapped[Optional["User"]] = relationship(back_populates="books")
    reviews: Mapped[List["Review"]] = relationship(
        back_populates="book", lazy="selectin"
    )
    tags: Mapped[List["Tag"]] = relationship(
        secondary=book_tag, back_populates="books", lazy="selectin"
    )

    def __repr__(self):
        return f"<Book {self.title}>"


class Review(Base):
    __tablename__ = "reviews"

    uid: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    rating: Mapped[int] = mapped_column()
    review_text: Mapped[str] = mapped_column(VARCHAR, nullable=False)
    user_uid: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.uid"), nullable=True
    )
    book_uid: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("books.uid"), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP, default=datetime.now)

    user: Mapped[Optional["User"]] = relationship(back_populates="reviews")
    book: Mapped[Optional["Book"]] = relationship(back_populates="reviews")

    def __repr__(self):
        return f"<Review for book {self.book_uid} by user {self.user_uid}>"
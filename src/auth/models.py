from sqlmodel import SQLModel, Field , Column
import sqlalchemy.dialects.postgresql as pg # for postgresql specific types , without this it will not work
import uuid
from datetime import datetime




class User(SQLModel, table=True):
    __tablename__ = "users"
    uid : uuid.UUID = Field(
        sa_column=Column(
            pg.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, nullable=False
        )
    )
    username: str
    email: str
    first_name: str
    last_name: str
    role: str = Field(sa_column=Column(pg.VARCHAR(50), nullable=False, default='user'))  # Default role is 'user'
    is_verified: bool = False
    password_hash: str = Field(exclude=True)  # Exclude from serialization
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP(timezone=True), nullable=False), default_factory=datetime.now)  # its an sqlalchemy column not a pydantic column
    updated_at: datetime = Field(sa_column=Column(pg.TIMESTAMP(timezone=True), nullable=False), default_factory=datetime.now)

    def __repr__(self):
        return f"<User {self.username}>"
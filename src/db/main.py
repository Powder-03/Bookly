from sqlmodel import create_engine , text , SQLModel
from sqlalchemy.ext.asyncio import AsyncEngine
from src.config import Config   
from src.books.models import Book
from src.auth.models import User
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker

engine = AsyncEngine(
    create_engine(
        url=Config.DATABASE_URL,
        echo=True,  # Set to True for SQL query logging
        )
)

async def init_db():
    async with engine.begin() as conn:
        # Here you can create tables or perform other database initialization tasks
        # For example, if you have models defined, you can use SQLModel's create_all method
        await conn.run_sync(SQLModel.metadata.create_all) 
        
        
async def get_session()-> AsyncSession:

    Session = sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False  # Set to False to avoid expiring objects after commit
    )
    
    async with Session() as session:
        yield session
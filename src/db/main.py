from sqlmodel import create_engine , text
from sqlalchemy.ext.asyncio import AsyncEngine
from src.config import Config   

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
        # await conn.run_sync(SQLModel.metadata.create_all)
        statement = text(
            "SELECT 'hello';"
        )
        
        result = await conn.execute(statement)
        print(result.all())  # This will print the result of the query
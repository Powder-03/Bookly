import redis.asyncio as redis
from src.config import Config


JTI_EXPIRY = 3600

token_blocklist = redis.Redis(
    host=Config.REDIS_HOST,
    port=Config.REDIS_PORT,
    db=0,  # Default database
)


async def add_jti_to_blocklist(jti:str)-> None:
    """Add a JWT ID (jti) to the blocklist."""
    await token_blocklist.set(name=jti,value="", ex=JTI_EXPIRY  )
    
    
async def token_in_blocklist(jti: str) -> bool:
    """Check if a JWT ID (jti) is in the blocklist."""
    exists = await token_blocklist.get(jti)
    return exists is not None  # Returns True if the jti exists in the blocklist

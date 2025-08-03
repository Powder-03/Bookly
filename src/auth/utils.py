from passlib.context import CryptContext
from datetime import timedelta ,  datetime
import jwt
from src.config import Config
import uuid
import logging


password_context = CryptContext(schemes=["bcrypt"])

ACCESS_TOKEN_EXPIRY = 3600


def generate_password_hash(password: str) -> str:
    """Generate a hashed password."""
    hash =  password_context.hash(password)
    return hash 


def verify_password(password : str ,  hash: str) -> bool:
    """Verify a password against a hashed password."""
    return password_context.verify(password, hash)


def create_access_token(user_data: dict ,  expiry: timedelta = None , refresh: bool = False) -> str:
    payload = {}
    
    payload['user'] = user_data
    payload['exp'] = datetime.now() + (expiry if expiry is not None else datetime.now() + timedelta(seconds=ACCESS_TOKEN_EXPIRY))
    payload['jti'] = str(uuid.uuid4())  
    
    payload['refresh'] = refresh
    
    
    token = jwt.encode(
        payload=payload,
        key=Config.JWT_SECRET,
        algorithm=Config.JWT_ALGORITHM,
    )
    
    return token


def decode_token(token: str) -> dict:
    try:
        # Decode the token to get the payload
        token_data = jwt.decode(
            jwt=token,
            key=Config.JWT_SECRET,
            algorithms=[Config.JWT_ALGORITHM],
        )
        return token_data
    except jwt.PyJWTError as e: # e is a variable that holds the exception object
        logging.exception(e)
        
        return None
from passlib.context import CryptContext

password_context = CryptContext(schemes=["bcrypt"])


def generate_password_hash(password: str) -> str:
    """Generate a hashed password."""
    hash =  password_context.hash(password)
    return hash 


def verify_password(password : str ,  hash: str) -> bool:
    """Verify a password against a hashed password."""
    return password_context.verify(password, hash)
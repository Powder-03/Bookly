from fastapi.security import HTTPBearer
from fastapi import Request
from fastapi.security.http import HTTPAuthorizationCredentials
from src.auth.utils import decode_token
from fastapi.exceptions import HTTPException, status

class AccessTokenBearer(HTTPBearer):
    
    def __init__(self, auto_error:bool = True): #if auto error is True, it will raise an error if the token is not provided 
        super().__init__(auto_error=auto_error)
        
        
    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        creds = await super().__call__(request)
        
        token = creds.credentials
        
        token_data = decode_token(token)
        if not self.token_valid:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token",
                headers={"WWW-Authenticate": "Bearer"},
            )
            
        if token_data['refresh']:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Refresh token is not allowed for this endpoint",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return token_data

    async def token_valid(self ,  token: str) -> bool:
        try:
            decoded_token = decode_token(token)
            return True if decoded_token else False
        except Exception as e:
            print(f"Token validation failed: {e}")
            return False
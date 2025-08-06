from fastapi.security import HTTPBearer
from fastapi import Request
from fastapi.security.http import HTTPAuthorizationCredentials
from src.auth.utils import decode_token
from fastapi.exceptions import HTTPException 
from fastapi import status , Depends
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from .service import UserService
from typing import List ,  Any
from src.auth.models import User

user_service = UserService()
    
from src.db.redis import token_in_blocklist

class TokenBearer(HTTPBearer):
    
    def __init__(self, auto_error:bool = True): #if auto error is True, it will raise an error if the token is not provided 
        super().__init__(auto_error=auto_error)
        
        
    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        creds = await super().__call__(request)
        
        token = creds.credentials
        
        token_data = decode_token(token)
        if not self.token_valid(token):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token",
                headers={"WWW-Authenticate": "Bearer"},
            )
            
        if await token_in_blocklist(token_data['jti']):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has been revoked",
                headers={"WWW-Authenticate": "Bearer"},
            )
            
        await self.verify_token_data(token_data)
        

        return token_data

    async def token_valid(self ,  token: str) -> bool:
        try:
            decoded_token = decode_token(token)
            return True if decoded_token else False
        except Exception as e:
            print(f"Token validation failed: {e}")
            return False
        
        
    async def verify_token_data(self, token_data: dict) -> None:
        
        raise NotImplementedError("Please override this method in child classes")
        
        

class AccessTokenBearer(TokenBearer):

    async def verify_token_data(self, token_data: dict) -> None:
        if token_data and not token_data['access']:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Please provide an access token",
                headers={"WWW-Authenticate": "Bearer"},
            )

    async def verify_token_data(self, token_data: dict) -> None:
        if token_data and not token_data['refresh']:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Please provide a refresh token",
                headers={"WWW-Authenticate": "Bearer"},
            )
        



class RefreshTokenBearer(TokenBearer):
    
    def verify_token_data(self , token_data:dict)->None:
        
        if token_data and not token_data['refresh']:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Please provide a refresh token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    
    

async def get_current_user(token_details: dict = Depends(AccessTokenBearer()) , session: AsyncSession = Depends(get_session)):
    """
    Dependency to get the current user based on the access token.
    This can be used in routes to ensure the user is authenticated.
    """
    user_email = token_details['user']['email']
    
    user = await user_service.get_user_by_email(user_email)
    
    return user


class RoleChecker:
    def __init__(self , allowed_roles: List[str]) -> None:
        
        self.allowed_roles = allowed_roles

    async def __call__(self , current_user: User = Depends(get_current_user)) -> Any:
        """
        Dependency to check if the current user has one of the allowed roles.
        This can be used in routes to ensure the user has the required role.
        """
        if current_user.role in self.allowed_roles:
            return True
        
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to perform this action",
            headers={"WWW-Authenticate": "Bearer"},
        )
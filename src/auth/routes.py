from fastapi import APIRouter, status, HTTPException, Depends
from .schemas import UserCreateModel, UserModel, UserLoginModel
from .service import UserService
from src.db.main import get_session
from .utils import create_access_token, decode_token, verify_password
from sqlmodel.ext.asyncio.session import AsyncSession
from datetime import timedelta , datetime
from fastapi.responses import JSONResponse     
from src.auth.dependencies import AccessTokenBearer , get_current_user , RoleChecker
import logging
from .dependencies import RefreshTokenBearer
from src.db.redis import add_jti_to_blocklist

auth_router = APIRouter()
user_service = UserService()
role_checker = RoleChecker(allowed_roles=['admin']) # This allows only admin users to access certain endpoints
# You can modify the allowed roles as per your requirements

REFRESH_TOKEN_EXPIRY = 2
access_token_bearer = AccessTokenBearer()


@auth_router.post('/signup', response_model=UserModel, status_code=status.HTTP_201_CREATED)
async def create_user_account(user_data: UserCreateModel, session: AsyncSession = Depends(get_session)):
    try:
        user_exists = await user_service.user_exists_by_email(user_data.email, session)
        if user_exists:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, 
                detail="User with this email already exists"
            )
        
        new_user = await user_service.create_user(user_data, session)
        return new_user
        
    except HTTPException:
        raise
    except Exception as e:
        logging.exception("Error creating user account")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create user account"
        )


@auth_router.post('/login')
async def login_users(login_data: UserLoginModel, session: AsyncSession = Depends(get_session)):
    try:
        email = login_data.email
        password = login_data.password
        
        user = await user_service.get_user_by_email(email, session)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        
        password_valid = verify_password(password, user.password_hash)
        if not password_valid:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        
        # Create tokens with consistent data
        user_data = {
            'email': user.email,
            'user_uid': str(user.uid),
            'role': user.role  # Include role in user data for token generation
        }
        
        access_token = create_access_token(user_data=user_data)
        
        refresh_token = create_access_token(
            user_data=user_data,
            refresh=True,
            expiry=timedelta(days=REFRESH_TOKEN_EXPIRY)
        )
        
        return JSONResponse(
            content={
                "message": "Login successful",
                "access_token": access_token,
                "refresh_token": refresh_token,
                "user": {
                    "email": user.email,
                    "uid": str(user.uid)
                }
            }
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logging.exception("Error during login")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Login failed"
        )


@auth_router.get('/refresh_token')
async def get_new_access_token(token_details:dict = Depends(RefreshTokenBearer())):
    expiry_timestamp = token_details['exp']
    
    if datetime.fromtimestamp(expiry_timestamp) > datetime.now():
        new_access_token = create_access_token(
            user_data=token_details['user'],
        )
        
        return JSONResponse(
            content={
                "access_token": new_access_token
            }
        )
        
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Refresh token has expired"
    )
# This endpoint generates a new access token if the refresh token is valid and not expired.
# It uses the RefreshTokenBearer dependency to validate the token and extract user data.
# If the refresh token is valid, it creates a new access token and returns it in the response.
# If the refresh token is expired, it raises an HTTPException with a 401 status code.
# The new access token is created with the same user data as the original token, ensuring
# that the user's identity remains consistent across tokens.
# The endpoint returns a JSON response containing the new access token and a success message.
# If the refresh token is expired, it raises an HTTPException with a 401 status code
# and a message indicating that the refresh token has expired.

@auth_router.get('/me')
async def get_current_user(user = Depends(get_current_user) , _:bool = Depends(role_checker)):
    return user

@auth_router.get('/logout')
async def revoke_token(token_details:dict = Depends(AccessTokenBearer())):
    
    jti = token_details['jti']
    
    await add_jti_to_blocklist(jti)
    
    return JSONResponse(
        content={
            "message": "Logged out successfully"
        },
        status_code=status.HTTP_200_OK
    )
from fastapi import APIRouter, status, HTTPException, Depends
from .schemas import UserCreateModel, UserModel , UserLoginModel
from .service import UserService
from src.db.main import get_session
from .utils import create_access_token , decode_token , verify_password
from sqlmodel.ext.asyncio.session import AsyncSession
from datetime import timedelta
from fastapi.responses import JSONResponse
from src.auth.dependencies import AccessTokenBearer



auth_router = APIRouter()
user_service = UserService()
REFRESH_TOKEN_EXPIRY= 2 
access_token_bearer = AccessTokenBearer()



@auth_router.post('/signup', response_model=UserModel, status_code=status.HTTP_201_CREATED)
async def create_user_account(user_data: UserCreateModel, session: AsyncSession = Depends(get_session)):
    
    user_exists = await user_service.user_exists_by_email(user_data.email, session)
    if user_exists:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User with this email already exists")
    
    new_user = await user_service.create_user(user_data, session)
    
    return new_user


@auth_router.post('/login')
async def login_users(login_data: UserLoginModel, session: AsyncSession = Depends(get_session)):
    email = login_data.email
    password = login_data.password
    
    user  = await user_service.get_user_by_email(email, session)
    if user is not None:
        password_valid = verify_password(password, user.password_hash)
        if password_valid:
            access_token = create_access_token(
                user_data={
                    'email': user.email,
                    'uid': user.uid,
                    'user_uid':str(user.uid)
                }
            )
            
            refresh_token = create_access_token(
                user_data={
                    'email': user.email,
                    'uid': user.uid,
                    'user_uid':str(user.uid)
                },
                refresh=True,
                expiry=timedelta(days=REFRESH_TOKEN_EXPIRY)
            )
            
            
            return JSONResponse(
                content={
                    "message":"Login Successful",
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "user":{
                        "email":user.email,
                        "uid": str(user.uid)
                    }
                }
            )
    
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Invalid Email or password"
    )

            
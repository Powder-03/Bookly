from .models import User
from sqlmodel.ext.asyncio.session import AsyncSession
from .utils import generate_password_hash
from .schemas import UserCreateModel
from sqlmodel import select




class UserService:
    async def get_user_by_email(self ,email: str ,  session: AsyncSession):
        statement = select(User).where(User.email == email)
        
        result = await session.exec(statement)
        user = result.first()
        return user
    
    
    async def user_exists_by_email(self, email: str, session: AsyncSession) -> bool:
        user = await self.get_user_by_email(email, session)
        
        if user is None:
            return False
        else:
            return True
        
        
    async def create_user(self , user_data: UserCreateModel, session: AsyncSession):
       
        user_data_dict = user_data.model_dump()
        # Remove password from dict and hash it separately
        password = user_data_dict.pop('password')
        
        new_user = User(**user_data_dict)
        new_user.password_hash = generate_password_hash(password)
        new_user.role = 'user'

        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return new_user
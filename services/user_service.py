from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from backend.database.models import User
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    name: str
    email: EmailStr

class UserService:
    @staticmethod
    async def create_user(session: AsyncSession, user: UserCreate):
        db_user = User(name=user.name, email=user.email)
        session.add(db_user)
        await session.commit()
        await session.refresh(db_user)
        return db_user

    @staticmethod
    async def get_user_by_id(session: AsyncSession, user_id: int):
        result = await session.execute(select(User).filter(User.id == user_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def update_user(session: AsyncSession, user_id: int, user_data: dict):
        result = await session.execute(select(User).filter(User.id == user_id))
        db_user = result.scalar_one_or_none()
        
        if db_user:
            for key, value in user_data.items():
                setattr(db_user, key, value)
            await session.commit()
            await session.refresh(db_user)
        
        return db_user

    @staticmethod
    async def delete_user(session: AsyncSession, user_id: int):
        result = await session.execute(select(User).filter(User.id == user_id))
        db_user = result.scalar_one_or_none()
        
        if db_user:
            await session.delete(db_user)
            await session.commit()
        
        return db_user is not None
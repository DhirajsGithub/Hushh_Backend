from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from backend.database.connection import get_async_session
from backend.services.user_service import UserService, UserCreate
from pydantic import BaseModel

router = APIRouter(prefix="/users", tags=["users"])

class UserResponse(BaseModel):
    id: int
    name: str
    email: str

@router.post("/", response_model=UserResponse)
async def create_user(
    user: UserCreate, 
    session: AsyncSession = Depends(get_async_session)
):
    try:
        created_user = await UserService.create_user(session, user)
        return UserResponse(
            id=created_user.id, 
            name=created_user.name, 
            email=created_user.email
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int, 
    session: AsyncSession = Depends(get_async_session)
):
    user = await UserService.get_user_by_id(session, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserResponse(
        id=user.id, 
        name=user.name, 
        email=user.email
    )
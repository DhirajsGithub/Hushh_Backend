from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from backend.database.models import Order, User
from pydantic import BaseModel
from typing import List

class OrderCreate(BaseModel):
    user_id: int
    product_name: str
    quantity: int

class OrderService:
    @staticmethod
    async def create_order(session: AsyncSession, order: OrderCreate):
        # Check if user exists
        user_result = await session.execute(select(User).filter(User.id == order.user_id))
        user = user_result.scalar_one_or_none()
        
        if not user:
            raise ValueError(f"User with ID {order.user_id} not found")
        
        # Create order
        db_order = Order(
            user_id=order.user_id, 
            product_name=order.product_name, 
            quantity=order.quantity
        )
        session.add(db_order)
        await session.commit()
        await session.refresh(db_order)
        
        return db_order

    @staticmethod
    async def get_orders_by_user(session: AsyncSession, user_id: int) -> List[Order]:
        result = await session.execute(
            select(Order).filter(Order.user_id == user_id)
        )
        return result.scalars().all()

    @staticmethod
    async def update_order(session: AsyncSession, order_id: int, order_data: dict):
        result = await session.execute(select(Order).filter(Order.id == order_id))
        db_order = result.scalar_one_or_none()
        
        if db_order:
            for key, value in order_data.items():
                setattr(db_order, key, value)
            
            await session.commit()
            await session.refresh(db_order)
        
        return db_order

    @staticmethod
    async def delete_order(session: AsyncSession, order_id: int):
        result = await session.execute(select(Order).filter(Order.id == order_id))
        db_order = result.scalar_one_or_none()
        
        if db_order:
            await session.delete(db_order)
            await session.commit()
        
        return db_order is not None
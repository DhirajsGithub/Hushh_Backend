from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from backend.database.connection import get_async_session
from backend.services.order_service import OrderService
from pydantic import BaseModel
from typing import List

router = APIRouter(prefix="/orders", tags=["orders"])

class OrderCreate(BaseModel):
    user_id: int
    product_name: str
    quantity: int

class OrderResponse(BaseModel):
    id: int
    user_id: int
    product_name: str
    quantity: int

@router.post("/", response_model=OrderResponse)
async def create_order(
    order: OrderCreate, 
    session: AsyncSession = Depends(get_async_session)
):
    try:
        created_order = await OrderService.create_order(session, order)
        return OrderResponse(
            id=created_order.id,
            user_id=created_order.user_id,
            product_name=created_order.product_name,
            quantity=created_order.quantity
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/user/{user_id}", response_model=List[OrderResponse])
async def get_user_orders(
    user_id: int, 
    session: AsyncSession = Depends(get_async_session)
):
    orders = await OrderService.get_orders_by_user(session, user_id)
    return [
        OrderResponse(
            id=order.id,
            user_id=order.user_id,
            product_name=order.product_name,
            quantity=order.quantity
        ) for order in orders
    ]
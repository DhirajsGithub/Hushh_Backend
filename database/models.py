from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    orders = relationship("Order", back_populates="user")

class Order(Base):
    __tablename__ = 'orders'
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    product_name = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    order_date = Column(DateTime(timezone=True), server_default=func.now())
    
    user = relationship("User", back_populates="orders")

class SearchClick(Base):
    __tablename__ = 'search_clicks'
    
    id = Column(Integer, primary_key=True, index=True)
    search_query = Column(String)
    clicks = Column(Integer, default=0)
    impressions = Column(Integer, default=0)
    click_through_rate = Column(Float)
    search_date = Column(DateTime(timezone=True), server_default=func.now())
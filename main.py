from fastapi import FastAPI
from backend.api import users, orders, llm_processing
from backend.database.connection import async_engine, Base
import uvicorn
import asyncio

app = FastAPI(
    title="Advanced Backend Application",
    description="Comprehensive Backend Solution with ML Integration",
    version="1.0.0"
)

# Include API routers
app.include_router(users.router)
app.include_router(orders.router)
app.include_router(llm_processing.router)

@app.on_event("startup")
async def startup():
    # Create database tables
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

if __name__ == "__main__":
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=True
    )
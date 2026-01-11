from typing import Generator
print('[dependencies.py] before SessionLocal imports')
from database import SessionLocal
print('[dependencies.py] after SessionLocal imports')
from database import AsyncSessionLocal
from sqlalchemy.orm import sessionmaker

def get_db() -> Generator[sessionmaker, None, None]:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

# https://medium.com/@rameshkannanyt0078/managing-database-connections-in-fastapi-best-practices-6f8404364936
async def get_async_db():
    async with AsyncSessionLocal() as session:
        yield session
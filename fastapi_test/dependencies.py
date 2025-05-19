from typing import Generator
from database import SessionLocal
from sqlalchemy.orm import sessionmaker

def get_db() -> Generator[sessionmaker, None, None]:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()
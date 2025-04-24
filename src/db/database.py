from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

url = "sqlite:///./src/db/test.db"
engine = create_engine(url)
DBSession = sessionmaker(bind=engine)

def get_db() -> Generator:
    db = DBSession()
    try:
        yield db
    finally:
        db.close()
from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from conf.env import settings

url = settings.DB_CONNECTION
engine = create_engine(url)
DBSession = sessionmaker(bind=engine)

def get_db() -> Generator:
    db = DBSession()
    try:
        yield db
    finally:
        db.close()
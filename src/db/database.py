from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

url = "sqlite:///./src/db/test.db"
engine = create_engine(url)
DBSession = sessionmaker(bind=engine)
print(type(DBSession()))
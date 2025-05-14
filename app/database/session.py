from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app.settings import settings

db_url = settings.db_url

engine = create_engine(db_url)

Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
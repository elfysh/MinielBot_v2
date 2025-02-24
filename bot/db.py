from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base
from config.config import DATABASE_URL

def get_session():
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()

    return session

def create_db():
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)
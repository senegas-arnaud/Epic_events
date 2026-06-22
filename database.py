from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URL
from models.base import Base
from models.collaborator import Collaborator
from models.client import Client
from models.contract import Contract
from models.event import Event

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def get_session():
    return SessionLocal()

def init_db():
    Base.metadata.create_all(engine)
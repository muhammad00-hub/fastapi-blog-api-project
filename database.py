from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

SQLALCHEMY_DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:Maqib@localhost:5432/blog_db"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)

Sessionlocal = sessionmaker(bind=engine)

Base = declarative_base()
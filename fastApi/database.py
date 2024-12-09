import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv

load_dotenv()

DB_USER = os.getenv("VITE_DATABASE_LOCAL_USER")
DB_PASSWORD = os.getenv("VITE_DATABASE_LOCAL_PASSWORD")
DB_NAME = os.getenv("VITE_DATABASE_LOCAL_NAME")
DB_HOST = os.getenv("VITE_DATABASE_LOCAL_HOST")
DB_PORT = os.getenv("VITE_DATABASE_LOCAL_PORT")

SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

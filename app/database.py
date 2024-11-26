import os
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

# SQLAlchemy Base object
Base = declarative_base()
engine = create_engine(os.getenv('DATABASE_URL'))
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv("db_uri")
connect_args_option = f'-c lock_timeout={os.getenv("LOCK_TIMEOUT")} -c statement_timeout={os.getenv("STATEMENT_TIMEOUT")}'

engine = create_engine(
    f"{SQLALCHEMY_DATABASE_URL}?{connect_args_option}",
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

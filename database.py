from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./blog.db"

engine=create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

local_session=sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base=declarative_base()

# SO NOW USING TABLE PLUS LETS CHOOSE SQLITE DATABASE, THEN LINK IT WITH THE blog.db file AND CREATE A TABLE NAMED BlogDatabase

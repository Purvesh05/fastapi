from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from psycopg import connect, ClientCursor
from psycopg.rows import dict_row
from .config import settings
import time


SQLALCHEMY_DATABASE_URL = f"postgresql+psycopg://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{int(settings.database_port)}/{settings.database_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# while True:
#     try:
#         # conn = psycopg2.connect(host="localhost",dbname="fastapi",
#         #                user="postgres",password="root@123", 
#         #                cursor_factory=RealDictCursor)
        
#         conn = connect(host="localhost",dbname="fastapi",
#                     user="postgres",password="root123", 
#                     cursor_factory=ClientCursor)

#         cursor = conn.cursor()
#         print("connected")
#         break

#     except Exception as error:
#         print("not connected")
#         print("Error: ",error)
#         time.sleep(2)  
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import DeclarativeBase
from dotenv import load_dotenv
import os

load_dotenv()

# SQLAlchemy
database_user = os.environ.get("Database_user")
database_password = os.environ.get("Database_password")
database_name = os.environ.get("Database_name")
database_host = os.environ.get("Database_host")
database_port = os.environ.get("Database_port")
#engine object to connect to db
engine = create_async_engine(
    url= 'postgresql+asyncpg://' + database_user + ":" + database_password + "@" + database_host + ":" + database_port + "/" + database_name,
    echo = True
)

#base class for creating database models
class Base(DeclarativeBase):
    pass

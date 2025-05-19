import datetime
import json
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
#import psycopg2

ECHO = False

load_dotenv()

hostname = os.environ.get("POSTGRES_HOST", "db")
user = os.environ.get("POSTGRES_USER", "casinouser")
password = os.environ.get("POSTGRES_PASSWORD", "12345678")
port = os.environ.get("POSTGRES_PORT", "5432")
db_schema_name = os.environ.get("POSTGRES_DB", "casino")

db_base_url = (
    "postgresql://"
    + user
    + ":"
    + password.replace("%", "%%")
    + "@"
    + hostname
    + ":"
    + str(port)
    + "/"
)

db_base_url_withoutpass = ("postgresql://" + user + "@" + hostname + ":" + str(port) + "/")

db_url = db_base_url + db_schema_name
db_url_withoutpass = db_base_url_withoutpass + db_schema_name

print(f"Connecting to db: {db_url_withoutpass}")

# Create database connection
engine = create_engine(
    db_url,
    echo=ECHO,
    pool_size=100,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=1800,
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# Create Base class for all models
class BaseWithRepr(object):
    def __repr__(self):
        attributes = {
            c.key: getattr(self, c.key)
            for c in self.__table__.columns
            if c.key in self.__dict__
        }
        for key in attributes:
            if isinstance(attributes[key], datetime.datetime):
                attributes[key] = attributes[key].strftime("%Y-%m-%d %H:%M:%S")
            elif isinstance(attributes[key], datetime.timedelta):
                attributes[key] = str(attributes[key])
        return json.dumps(attributes, indent=4)


Base = declarative_base(cls=BaseWithRepr)
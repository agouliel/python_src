import os
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import DeclarativeBase, sessionmaker

class Model(DeclarativeBase):
    metadata = MetaData(naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    })

# https://docs.sqlalchemy.org/en/20/dialects/mssql.html#connecting-to-pyodbc
# When using a hostname connection, the driver name must also be specified
engine = create_engine(f"mssql+pyodbc://dataminer:{os.environ['SERVDBPASS']}@localhost/CodeFirstDB?driver=ODBC+Driver+17+for+SQL+Server")

Session = sessionmaker(engine)
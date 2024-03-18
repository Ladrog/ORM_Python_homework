import sqlalchemy
from sqlalchemy.orm import sessionmaker

from ORM_models import create_tables

DSN = 'postgresql://postgres:123@localhost:5432/bookstore_db'
engine = sqlalchemy.create_engine(DSN)

create_tables(engine)

Session = sessionmaker(bind=engine)
session = Session()

session.close()
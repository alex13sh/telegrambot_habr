from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker 

engine = create_engine('sqlite:///:memory:', echo=True)
Session = scoped_session(sessionmaker(bind=engine))
def init_base():
    Base.metadata.create_all(engine)

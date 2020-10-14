import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, TIMESTAMP, String

Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True

    id = Column(Integer, nullable=False, unique=True, primary_key=True, autoincrement=True)
    created_at = Column(TIMESTAMP, nullable=False, default=datetime.datetime.now())
    updated_at = Column(TIMESTAMP, nullable=False, default=datetime.datetime.now(), onupdate=datetime.datetime.now())

    def __repr__(self):
        return "<{0.__class__.__name__}(id={0.id!r})>".format(self) 

class MediaCache(Base):
    __tablename__ = 'MediaCache'
    
    url = Column(String(255), unique=True, nullable=False, primary_key=True)
    media_id = Column(String(255), nullable=False)
    
    created_at = Column(TIMESTAMP, nullable=False, default=datetime.datetime.now())

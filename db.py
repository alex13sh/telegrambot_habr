from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class BD_Subs(Base):
    __tablename__ = 'BD_Subs'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    sub_name = Column(String(255)) 


from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker 
engine = create_engine('sqlite:///:memory:', echo=True)

Base.metadata.create_all(engine)
Session = scoped_session(sessionmaker(bind=engine))

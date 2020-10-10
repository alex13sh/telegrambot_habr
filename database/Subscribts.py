from db import Base, session
from db import ForeignKey, Column, Integer, String, Text

from .base import BaseModel

class BD_Subs(Base):
    __tablename__ = 'BD_Subs'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    sub_name = Column(String(255))
    #sms_id = Column(Integer)
    
class BD_Subs_SMS(Base):
    __tablename__ = 'BD_Subs_SMS'
    sms_id = Column(Integer, primary_key=True)
    #subs_id = Column(Integer)
    subs_id = Column(ForeignKey('BD_Subs.id', ondelete='CASCADE'), nullable=False, index=True)
    
def new_subs(user_id, sub_name, sms_id=None):
    row = BD_Subs(user_id=user_id, sub_name=sub_name)
    session.add(row)
    session.commit()
    #session.refresh(row)
    if sms_id:
        session.add(BD_Subs_SMS(sms_id=sms_id, subs_id=row.id))
        session.commit()

class Subscribs(BaseModel):
    __tablename__ = 'Subscribs'
    
    web_host = Column(String(50), nullable=False)
    url = Column(String(255))
    sub_type = Column(String(20), nullable=False)
    sub_name = Column(String(50))
    last_title_id = Column(ForeignKey('Titles.id'), index=True)
    
class User_Sub(BaseModel):
    __tablename__ = 'User_Sub'
    
    user_id = Column(Integer)
    sub_id = Column(ForeignKey('Subscribs.id', ondelete='CASCADE'), nullable=False, index=True)
    
class Titles(BaseModel):
    __tablename__ = 'Titles'
    
    sub_id = Column(ForeignKey('Subscribs.id', ondelete='CASCADE'), nullable=False, index=True)
    url = Column(String(255), nullable=False)
    image_url = Column(String(255))
    #image_id 
    title = Column(String(255), nullable=False)
    text = Column(Text, nullable=False)
    
class MediaCache(BaseModel):
    __tablename__ = 'MediaCache'
    
    url = Column(String(255), unique=True, nullable=False)
    media_id = Column(String(255), nullable=False)

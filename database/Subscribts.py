from db import Base, session
from db import relationship, ForeignKey, column_property
from db import Column, Integer, String, Text

from .base import BaseModel, MediaCache

class BD_Subs_SMS(Base):
    __tablename__ = 'BD_Subs_SMS'
    
    sms_id = Column(Integer, primary_key=True)
    subs_id = Column(ForeignKey('BD_Subs.id', ondelete='CASCADE'), nullable=False, index=True)
    sub = relationship("BD_Subs", back_poplates = "sms", cascade='all,delete')

class BD_Subs(Base):
    __tablename__ = 'BD_Subs'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    sub_name = Column(String(255))
    
    sms = relationship("BD_Subs_SMS", backref = "sub", cascade='all,delete')
    
    @classmethod
    def new_subs(cls, user_id, sub_name, sms_id=None):
        row = cls(user_id=user_id, sub_name=sub_name)
        if sms_id:
            row.sms.append(BD_Subs_SMS(sms_id=sms_id))
        session.add(row)
        session.commit()

    @classmethod
    def del_subs_sms_id(cls, sms_id):
        try:
            res = session.query(BD_Subs_SMS).filter_by(sms_id=sms_id).one()
            print("Result subs_id:", res.subs_id)
            session.delete(res.sub)
            session.commit()
            return res
        except:
            session.rollback()
            return None
    
    @classmethod
    def is_sub(cls, user_id, sub_name):
        return len (session.query(BD_Subs).filter_by(user_id=user_id, sub_name=sub_name).all()) > 0

    @classmethod
    def get_users_sub(cls, sub_name):
        return session.query(BD_Subs.user_id).filter_by(sub_name=sub_name).all()
        
    @classmethod
    def list_sub(cls):
        pass

    

class Subscribs(BaseModel):
    __tablename__ = 'Subscribs'
    
    parser_id = Column(ForeignKey('Parsers.id', ondelete='CASCADE'), nullable=False, index=True)
    #web_host = Column(String(50), nullable=False)
    #url = Column(String(255))
    #sub_type = Column(String(20), nullable=False)
    sub_name = Column(String(50))
    last_title_id = Column(ForeignKey('Titles.id'), index=True)
    
    #users = relationship("User_Sub", backref = "sub", cascade='all,delete')
    #titles = relationship("Titles", backref = "sub", cascade='all,delete')
    
class User_Sub(BaseModel):
    __tablename__ = 'User_Sub'
    
    user_id = Column(Integer)
    sub_id = Column(ForeignKey('Subscribs.id', ondelete='CASCADE'), nullable=False, index=True)
    
class Titles(BaseModel):
    __tablename__ = 'Titles'
    
    sub_id = Column(ForeignKey('Subscribs.id', ondelete='CASCADE'), nullable=False, index=True)
    url = Column(String(255), nullable=False)
    
    #images = relationship("MediaCache", backref = "title", cascade='all,delete')
    title = Column(String(255), nullable=False)
    text = Column(Text, nullable=False)
    

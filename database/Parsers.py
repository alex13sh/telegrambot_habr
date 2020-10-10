from db import Base, Session, session
from db import Column, Integer, String, Text

from .base import BaseModel

class Parsers(BaseModel):
    __tablename__ = 'Parsers'
    
    web_host = Column(String(50), nullable=False)
    url = Column(String(255))
    sub_type = Column(String(20), nullable=False)
    script = Column(String(50), nullable=False)

def fill():
    session.add(Parsers(web_host='https://stopgame.ru', url='https://stopgame.ru/review/new', sub_type="game_new", script="./*/stopgame.py"))
    session.add(Parsers(web_host='https://habr.com', url='https://habr.com/ru/all/', sub_type="all", script="./*/habr.py"))
    
    session.commit()
    

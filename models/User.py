from sqlalchemy import Column, Integer, String
from database import Base
from pass_manager import Secrets


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    password = Column(String(50))
    secret = Secrets()

    def __init__(self, name, pass_word):
        self.name = name
        self.password = self.secret.hash_password(pass_word, 14)

    def __repr__(self):
        return '<User %r>' % self.name

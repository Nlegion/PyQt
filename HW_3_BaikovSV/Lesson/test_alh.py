from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData
from sqlalchemy.orm import mapper
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(32))
    fullname = Column(String(64))
    password = Column(String(128))

    def __init__(self, name, fullname, password):
        self.name = name
        self.fullname = fullname
        self.password = password

    def __repr__(self):
        return f'{self.__class__.__name__}({self.name},{self.fullname},{self.password})'


engine = create_engine('sqlite:///my_bd.sqlite', echo=True)
Base.metadata.create_all(engine)

user_1 = User('test', 'testes', 'tesss')
print(user_1)

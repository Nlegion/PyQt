import sys

try:
    import sqlalchemy

    print(sqlalchemy.__version__)
except ImportError:
    print('Ошибка')
    sys.exit(1)
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData
from sqlalchemy.orm import mapper

engine = create_engine('sqlite:///my_bd.sqlite', echo=True)
print(engine)
metadata = MetaData()

user_table = Table(
    'users', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(64)),
    Column('fullname', String),
    Column('password', String),
)

metadata.create_all(engine)


class User:
    def __init__(self, name, fullname, password):
        self.name = name
        self.fullname = fullname
        self.password = password

    def __repr__(self):
        return f'{self.__class__.__name__}({self.name},{self.fullname},{self.password})'


user_m = mapper(User, user_table)
print(user_m)

user_1 = User('test', 'testes', 'tesss')
print(user_1)

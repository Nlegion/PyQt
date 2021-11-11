from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import declarative_base
import datetime

Base = declarative_base()


class AllUsers(Base):
    __tablename__ = 'all_users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    last_login = Column(DateTime)
    password = Column(String)

    def __init__(self, username, last_login, password):
        self.username = username
        self.last_login = last_login
        self.password = password

    def __repr__(self):
        return f'<User({self.username}, {self.last_login}, {self.password})>'


class UsersContacts(Base):
    __tablename__ = 'users_contacts'
    id = Column(Integer, primary_key=True)
    username = Column(ForeignKey('all_users.id'))
    contact = Column(String)
    last_msg = Column(DateTime)

    def __init__(self, username, contact, last_msg):
        self.username = username
        self.contact = contact
        self.last_msg = last_msg

    def __repr__(self):
        return f'<User({self.username}, {self.contact}, {self.last_msg})>'


class LoginHistory(Base):
    __tablename__ = 'users_login_history'
    id = Column(Integer, primary_key=True)
    username = Column(ForeignKey('all_users.id'))
    login_time = Column(DateTime)
    ip_address = Column(String)
    port = Column(Integer)

    def __init__(self, username, login_time, ip_address, port):
        self.username = username
        self.login_time = login_time
        self.ip_address = ip_address
        self.port = port

    def __repr__(self):
        return f'<User({self.username}, {self.login_time}, {self.ip_address}, {self.port})>'


if __name__ == '__main__':
    engine = create_engine('sqlite:///my_bd.sqlite', echo=True)
    Base.metadata.create_all(engine)

    user_1 = AllUsers("User1", '192.168.1.4', '123')
    contact_1 = UsersContacts("User1", "User1", "smth")
    log_hist_1 = LoginHistory("User1", datetime.datetime.now(), None, None)

    print(user_1, contact_1, log_hist_1)

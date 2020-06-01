from sqlalchemy import create_engine, Table, Column, Boolean, Integer, String, ForeignKey, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.pool import QueuePool
"""
from sqlalchemy.dialects. import \
    BFILE, BLOB, CHAR, CLOB, DATE, \
    DOUBLE_PRECISION, FLOAT, INTERVAL, LONG, NCLOB, \
    Integer, NVARCHAR, NString, TIMESTAMP, VARCHAR, \
    String
"""
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import time
from datetime import date
import uuid
import os

os.environ['LD_LIBRARY_PATH'] = "/usr/lib/oracle/18.5/client64/lib"
os.environ['ORACLE_HOME'] = "/usr/lib/oracle/18.5/client64/"

engine = create_engine('postgresql+pg8000://postgres:postgres@localhost/cherry', max_identifier_length=128, \
                       echo=False)
Session = sessionmaker(bind=engine)
Base = declarative_base()
session = Session(autocommit=True,autoflush=True)
#cursor = engine.connect()

class User(UserMixin, Base):
    
    __tablename__ = 'user'
    
    
    id = Column(String(255), primary_key=True)
    nickname = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    
    def __init__(self, nickname, password):
        self.nickname = nickname
        self.password = generate_password_hash(password)
        self.id = str(uuid.uuid4())
        
    def __repr__(self):
        return self.nickname
    
    def get_id(self):
        return self.id
    
    def create_activity(self):
        return Activity(self)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def password_check(self, password):
        return check_password_hash(self.password, password)

class Status(Base):
    
    __tablename__ = 'status'
    
    id = Column(String(255), primary_key=True)
    
    user_id = Column(String(255), ForeignKey('user.id'), nullable=False)
    
    status = Column(Boolean,default=False,nullable=False)
    
    device = Column(String(255), nullable=True)
    
    def __init__(self, User, device="127.0.0.1"):
        self.id = str(uuid.uuid4())
        self.user_id = User.get_id()
        self.status = True
        self.device = device
        
    def __repr__(self):
        return str(self.status) + ':' + str(self.device)
    
    def logout(self):
        self.status = False
        
    def login(self):
        self.status = True

class Role(Base):
    
    __tablename__ = 'role'
    
    id = Column(String(255), ForeignKey('user.id'), primary_key=True, nullable=False)
    role = Column(String(255),default="guest", primary_key=True, nullable=False)
    roles = ['admin', 'teacher', 'student','guest']
    
    def __init__(self,User):
        self.id = User.get_id()
        
    def add_role(self, role):
        if role in self.roles:
            self.role = role
    
    def check_role(self, User, role):
        roles = session.query(Role).filter_by(id=User.get_id()).all()
        return any(i.role == role for i in roles)
    
class Post(Base):
    
    __tablename__ = 'post'
    
    id = Column(String(255), primary_key=True)
    
    user_id = Column(String(255), ForeignKey('user.nickname'))
    
    body = Column(String(255))
    
    date = Column(Integer)
    
    def __init__(self, User, body):
        self.id = str(uuid.uuid4())
        
        self.date = time.time()
        
        self.body = body
        
        self.user_id = User.nickname
        
    def __repr__(self):
        
        return self.body

class Activity(Base):
    
    __tablename__ = 'activity'
    
    id = Column(String(255), ForeignKey('user.id'), primary_key=True, nullable=False)

    activity_count = Column(Integer, default=0)
    lastActivity = Column(String(255))
    
    def __init__(self, User):
        
        self.id = User.get_id()
        print("ACTIVITY_EVENT")
        self.lastActivity = str(date.today())
        
    def activity_event(self):
        
        self.lastActivity = str(date.today())
        
        self.activity_count += 1
        
'''
class Teacher(Base):
    
    __tablename__ = 'user'
    
    id = Column(String(255), ForeignKey('user.id'), primary_key=True)
    
    experience_body = Column(String(255))
    
    position = Column(String(255))
    
    experience_years = Column(String(255))
    
    photo = Column(String(255))
    
    def __init__(self, User):
        self.id = User.get_id()
        
'''


Base.metadata.create_all(engine)
print(engine.table_names())


a = User("test","test")
session.add(a)
#session.flush()
#session.add(c)

#b = a.create_activity()
#session.add(b)
#session.flush()
#session.add(Role(a.get_id(), ['admin']))
#.commit()
#session.flush()
#session.close()
#print(a.get_id())
from sqlalchemy import create_engine, Table, Column, Boolean, Integer, String, ForeignKey, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.pool import QueuePool
from sqlalchemy.dialects.oracle import \
    BFILE, BLOB, CHAR, CLOB, DATE, \
    DOUBLE_PRECISION, FLOAT, INTERVAL, LONG, NCLOB, \
    NUMBER, NVARCHAR, NVARCHAR2, RAW, TIMESTAMP, VARCHAR, \
    VARCHAR2
import binascii
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import time
from datetime import date
import uuid
import os

os.environ['LD_LIBRARY_PATH'] = "/usr/lib/oracle/18.5/client64/lib"
os.environ['ORACLE_HOME'] = "/usr/lib/oracle/18.5/client64/"

engine = create_engine('oracle+cx_oracle://cherry:mypassword@localhost:51521/xe', max_identifier_length=128, \
                       echo=False)
Session = sessionmaker(bind=engine)
Base = declarative_base()
session = Session(autocommit=True)
cursor = engine.connect()

class User(UserMixin, Base):
    __tablename__ = 'user'
    
    id = Column(VARCHAR2(255), primary_key=True)
    nickname = Column(VARCHAR2(20), unique=True, nullable=False)
    password = Column(VARCHAR2(100), nullable=False)
    
    def __init__(self, nickname, password):
        self.nickname = nickname
        self.password = generate_password_hash(password)
        self.id = str(uuid.uuid4())
        
    def __repr__(self):
        return self.nickname
    
    def get_id(self):
        return self.id
    
    def password_check(self, password):
        return check_password_hash(self.password, password)
    
        
class Role(Base):
    __tablename__ = 'role'
    
    id = Column(VARCHAR2(255), ForeignKey('user.id'), primary_key=True)
    
    roles = ['admin', 'teacher', 'student']
    for i in roles:
        exec(i + ' = Column(Boolean,default=False,nullable=False)')
    
    def __init__(self,id, args):
        print(id)
        self.id = id
        print(args)
        for i in args:
            if i in self.roles:
                exec("self." + i + " =True")


class Post(Base):
    __tablename__ = 'post'
    
    id = Column(VARCHAR2(255), primary_key=True)
    
    user_id = Column(VARCHAR2(255), ForeignKey('user.id'))
    
    body = Column(VARCHAR2(255))
    
    date = Column(NUMBER)
    
    def __init__(self, body, user_id):
        self.id = str(uuid.uuid4())
        
        self.date = time.time()
        
        self.body = body
        
        self.user_id = user_id


class Activity(Base):
    __tablename__ = 'activity'
    
    id = Column(VARCHAR2(255), ForeignKey('user.id'), nullable=False)

    activity_count = Column(NUMBER, default=0)
    lastActivity = Column(VARCHAR2(255))
    
    def __init__(self, User):
        
        self.id = User.get_id()
        
        self.lastActivity = str(date.today())
        
    def activity_event(self):
        
        self.lastActivity = str(date.today())
        
        self.activity_count += 1
        

Base.metadata.create_all(engine)
print(engine.table_names())

a = User("gay","gay")
session.add(a)
#session.flush()
#session.add(Role(a.get_id(), ['admin']))
#.commit()
#session.flush()
#session.close()
print(a.get_id())

"""
class Student(Base):
    __tablename__ = 'student'
    
    id = Column(NUMBER, primary_key=True, autoincrement=True)
    name = Column(VARCHAR2(30), nullable=False)
    surname = Column(VARCHAR2(30), nullable=False)
    group = Column(VARCHAR2(30), nullable=False)
    math = Column(NUMBER)
    nature = Column(NUMBER)
    programming = Column(NUMBER)
    
    def __init__(self, name, surname, group, math=0, nature=0, programming=0):
        self.name = name
        self.surname = surname
        self.group = group
        self.math = math
        self.nature = nature
        self.programming = programming
    
    def __repr__(self):
        return self.name + ' ' + self.surname
"""




#Base.metadata.create_all(engine)

'''
class Disciplines(Base):
	__tablename__ = 'disciplines'
	
	id = Column(NUMBER, primary_key=True, autoincrement=True)
	discipline = Column(VARCHAR2(30), nullable=True, unique=True)
	name = Column(VARCHAR2(30), nullable=False, unique=True)
	path = Column(VARCHAR2(70), nullable=False, unique=True)
	
	def __init__(self, discipline, name, path='/home/vlados/kurs/files'):
		self.discipline = discipline
		self.name = name
		self.path = os.path.join(path + '/' + discipline, name)
	
	def __repr__(self):
		return self.discipline + ' : ' + self.name
'''

# session.add(User('hueta', 'lolkek'))
# session.commit()
# session.close()
# print((session.execute(text("SELECT nickname FROM user")).first()).nickname) - works
# print((tuple(('gay',)) in (session.execute(text("SELECT nickname FROM user")).fetchall())))
# print(((session.query(User.nickname).filter_by(nickname = 'gay').all().nickname)))
# print(type('sar'))
'''
username = 'gay',
password = 'gay',
if (username + password) in (session.execute(text("SELECT nickname, password FROM user"))).fetchall():
	print('hello')
else:
	print(username + password)
	print(session.execute(text("SELECT nickname, password FROM user")).fetchall())
'''
# update
'''
Session = sessionmaker(bind = engine)
session = Session()
session.commit()
'''
# print(str(session.dirty()) + ' ' + 'DIRTY THIGS WAS MADE ' )

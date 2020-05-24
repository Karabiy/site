from sqlalchemy import create_engine, Table, Column, Boolean, Integer, String, ForeignKey, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.pool import QueuePool
from sqlalchemy.dialects.oracle import \
    BFILE, BLOB, CHAR, CLOB, DATE, \
    DOUBLE_PRECISION, FLOAT, INTERVAL, LONG, NCLOB, \
    NUMBER, NVARCHAR, NVARCHAR2, RAW, TIMESTAMP, VARCHAR, \
    VARCHAR2

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import os

os.environ['LD_LIBRARY_PATH'] = "/usr/lib/oracle/18.5/client64/lib"
os.environ['ORACLE_HOME'] = "/usr/lib/oracle/18.5/client64/"

engine = create_engine('oracle+cx_oracle://cherry:mypassword@localhost:51521/xe', echo=False, \
                       max_identifier_length=128)
Session = sessionmaker(bind=engine)
Base = declarative_base()
session = Session(autocommit=True)
cursor = engine.connect()

class User(UserMixin, Base):
    __tablename__ = 'user'
    
    id = Column(NUMBER, primary_key=True, autoincrement=True, default=int(1))
    nickname = Column(VARCHAR2(20), unique=True, nullable=False)
    password = Column(VARCHAR2(100), nullable=False)
    
#    post = relationship('Post', back_populates='id', cascade="all, delete, delete-orphan")
#    role = relationship('Role', back_populates='id', cascade="all, delete, delete-orphan")
    
    def __init__(self, nickname, password):
        self.nickname = nickname
        self.password = generate_password_hash(password)
    
    def __repr__(self):
        return self.nickname
    
    def get_id(self):
        return self.id
    
    def password_check(self, password):
        return check_password_hash(self.password, password)


class Role(Base):
    __tablename__ = 'role'
    
    id = Column(NUMBER, ForeignKey('user.id'), primary_key=True, nullable=False)
    
    roles = ['admin', 'teacher', 'student']
    for i in roles:
        exec(i + ' = Column(Boolean,default=False,nullable=False)')
    
    def __init__(self,id, args):
        self.id = int(id)
        print(args)
        for i in args:
            if i in self.roles:
                exec("self." + i + " =True")


'''
class Activity(Base):
	
	__tablename__ = 'activity'
	
	activity = Column(NUMBER)
	lastActivity = Column(VARCHAR2(255))
'''


class Post(Base):
    __tablename__ = 'post'
    
    post_id = Column(NUMBER, primary_key=True)
    post_data = Column(VARCHAR2(255), nullable=False)
    nickname = Column(VARCHAR2(20), ForeignKey('user.nickname'), nullable=False)
    
    #user = relationship("user", order_by=User.id, back_populates='post')
    
    def __init__(self, post_data, User):
        self.post_data = post_data
        self.nickname = User.nickname
        User.activity += 1
    
    def __repr__(self):
        return self.post_data + '@ by ' + self.nickname

Base.metadata.create_all(engine)
print(engine.table_names())

session.add(Role(int(1), ['admin']))
#.commit()
session.flush()
#session.close()
print(session.query(User).all())
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

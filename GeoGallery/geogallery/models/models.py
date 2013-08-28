from sqlalchemy import (
    Column,
    Integer,
    Text,
    String,
    DateTime,
    Unicode,
    Boolean,
    )

import datetime
from sqlalchemy.orm import relationship, backref

from sqlalchemy.ext.associationproxy import association_proxy

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )
from sqlalchemy.schema import Table, ForeignKey

from zope.sqlalchemy import ZopeTransactionExtension

from pyramid.security import (
    Allow,
    Everyone,
    )

class RootFactory(object):
    __acl__ = [ (Allow, Everyone, 'user'),
                (Allow, 'g:admin', 'admin') ]
    def __init__(self, request):
        pass
DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()

user_groups = Table('user_groups', Base.metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('group_id', Integer, ForeignKey('groups.id')))

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(Unicode(100), nullable=False, unique=True)
    name = Column(Unicode(80), nullable=False)
    email = Column(String(100))
    age = Column(Integer)

    def __init__(self, username, name, email, age):
        self.username = username
        self.name = name
        self.email = email
        self.age = age

class Roles(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True, autoincrement=True)
    role_name = Column(Unicode(20), nullable=False)
    
    def __init__(self, role_name):
        self.role_name = role_name

class UserRole(Base):
    __tablename__ = 'user_roles'
    id = Column(Integer, primary_key=True, autoincrement=True)
    role_id = Column(Integer, ForeignKey('roles.id'))
    user_id = Column(Integer, ForeignKey('users.id'))


    def __init__(self, role_id, user_id):
        self.role_id = role_id
        self.user_id = user_id
        
class Group(Base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(40), nullable = False)

    def __init__(self, name):
        self.name = name


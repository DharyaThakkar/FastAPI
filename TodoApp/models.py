#models is a way for sqlalchemy to understand what kind of database tables we going to create in the future.

from .database import Base
from sqlalchemy import Column,Integer,String,Boolean,ForeignKey


class Users(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True) #index = True will make retrieval a little bit more efficient from the database.
    email = Column(String, unique=True)
    username = Column(String,  unique=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String) #storing the password of the users in a hashed way(encrypted format) which cannot be decrypted.
    is_active = Column(Boolean,default=True)
    role = Column(String) 
    phone_number = Column(String, nullable=False)
    
    
    

#so this will helps us to create a table of Todos.
class Todos(Base):
    __tablename__ = 'todos'
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey('users.id'))
    
    
    
    
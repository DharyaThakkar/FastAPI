#Here we will create the URL string which will connect our FastAPI application to the database.
from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker

from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL = "sqlite:///./todosapp.db" #This URL is going to create the location of this database in our fastAPI application.(locationpata hoga tabhi to connect kar paayega guru !)


#SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:Dharya%40321@localhost/TodoApplicationDatabase'

# SQLALCHEMY_DATABASE_URL = 'mysql+pymysql://root:Dharya%40321@127.0.0.1:3306/TodoApplicationDatabase'


#The next thing we need is engine for our application.Our databse engine is something which we can use to open up a connection and able to use our database.
# engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread' : False}) #inside the create engine we have to add the database path for our database. 

engine = create_engine(SQLALCHEMY_DATABASE_URL)

#connect_args will help us to define some kind of connection to a Database.By-default , sqlite will only allows one thread to communicate with database.Assuming that each thread will handle an independent request.The reason why we are using 'check_same_thread':False.
#so we are doing it for preventing any kind of the accidental sharing of the same connection for different kind of requests.


#Now we are going to create sessionlocal and each instance of the sessionlocal will have a database session.

SessionLocal = sessionmaker(autoflush=False,autocommit=False, bind=engine)#This will allows us to have a fully controlled over the database system.

#Now the last thing which we need to do is to create a database object using which we can interact later on. 

Base = declarative_base() #This is the object of the database which will be then controlling our database.


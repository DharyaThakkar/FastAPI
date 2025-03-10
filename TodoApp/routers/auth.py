from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from ..models import Users
from passlib.context import CryptContext
from ..database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from starlette import status
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer  #we now need to use it as a DI for our API endpoint.
from jose import JWTError, jwt
from fastapi.templating import Jinja2Templates

router = APIRouter(
    prefix='/auth',
    tags=['auth'] #we are now going to divide our application with a new title of auth and that will show all the auth api's and each api endpoint within this  auth file is going to start with '/auth'.
)

SECRET_KEY = 'SOME KEY' #Now a jwt means a secret and it needs an algorithm,

ALGORITHM = 'HS256' #signature and algorithm will work together to add a signature to the  JWT to make sure that JWT is secured and authorized.

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto') #now inside the bcrypt_context , we are going to use the hashing algorithm of 'bcrypt'.we have installed bycrypt of version 4.0.1, so we can work with the passlib.

oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token') #In the header of every api endpoint, we are going to pass this bearertoken which is a jwt and we are telling our fastapi to check this jwt before we process the request.
#toeknUrl = 'token' specifies the URL endpoint where clients can obtain a Bearer token.

class CreateUserRequest(BaseModel): #Creating a pydantic UserRequestModel for validation of the fields of the User Model and then storing the record in the database.
    username:str
    email:str
    first_name:str
    last_name:str
    password:str
    role:str
    phone_number:str


class Token(BaseModel):
    access_token:str
    token_type:str
     

def get_db():
    #This is not now a normal function, it is a generator function which can be iterated over to yield the value generated by the function.
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
db_dependency = Annotated[Session, Depends(get_db)] #The Annotated type with Depends(get_db) handles session creation, injection, and cleanup.


templates = Jinja2Templates(directory='TodoApp/templates')


## Pages ##
@router.get('/login-page')
def render_login_page(request:Request):
    return templates.TemplateResponse('login.html', {'request' : request}) #same concept applies here, whenever we are rendering any HTML page, we have to accept a request as an argument and also need to send the request as an argument.


@router.get('/register-page')
def render_register_page(request:Request):
    return templates.TemplateResponse('register.html', {'request' : request})


## Endpoints ##
def authenticate_user(username:str, password:str,db):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user    


def create_access_token(username:str, user_id:int, role:str, expires_delta:timedelta):
    
    #inforamtion that lives inside the JWT , we can dictate it right here.
    encode = {'sub' : username, 'id':user_id, 'role':role}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({'exp' : expires})
    return jwt.encode(encode,SECRET_KEY,ALGORITHM)
  
#we cam also have async function inside the code which is actually not an API endpoint.  
async def get_current_user(token:Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        username : str = payload.get('sub')
        user_id : int = payload.get('id')
        user_role : str = payload.get('role') 
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='could not validate credentials')
        
        return {'username' : username, 'id' : user_id, 'user_role':user_role}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='could not validate credentials')
        
        
                   

@router.post('/',status_code=status.HTTP_201_CREATED)
async def create_user(db:db_dependency,create_user_request:CreateUserRequest): #db is not explicitly defined because it is injected by db_dependency. 
    create_user_model = Users(
        email=create_user_request.email,
        username=create_user_request.username,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        role = create_user_request.role,
        hashed_password = bcrypt_context.hash(create_user_request.password),
        is_active = True,
        phone_number=create_user_request.phone_number
    )
    db.add(create_user_model)
    db.commit() 
    
#This api endpoint is going to be a post request method with a path of '/token'.A token is what we are going to return back to the user , that's going to have all of the information about the user inside.
#This token is going to be a JWT(JSON Web Tokens).

@router.post('/token', response_model=Token)
async def login_for_access_token(form_data:Annotated[OAuth2PasswordRequestForm,Depends()], db:db_dependency):
    
    user = authenticate_user(form_data.username,form_data.password,db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='could not validate credentials')
    token = create_access_token(user.username,user.id,user.role,timedelta(minutes=20))
    return {'access_token':token, 'token_type':'bearer'}






    
    
    
    
    
    



#APIRouter will help us to route from main.py file to our auth.py file.  
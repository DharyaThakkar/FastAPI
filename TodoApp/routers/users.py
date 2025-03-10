from fastapi import APIRouter,Depends,HTTPException
from ..models import Todos,Users
from ..database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from pydantic import BaseModel,Field
from starlette import status
from .auth import get_current_user
from passlib.context import CryptContext


router = APIRouter(
    prefix='/user',
    tags=['user']
)


#creating db dependency :-

def get_db(): #Database Dependency Function.
    db = SessionLocal() #creates a new session.
    try:
        yield db #code prior to and including the yield statement is executed before sending a response
    finally:
        db.close() #the code following the yield statement is executed after the response has been delivered.
        
    
db_dependency =  Annotated[Session, Depends(get_db)]  #we are using Annotated for type hinting the Session as a dependency. 
user_dependency = Annotated[dict, Depends(get_current_user)]
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')



#creating a new pydantic class for user verification
class UserVerification(BaseModel):
    password : str
    new_password : str = Field(min_length=6)      

@router.get('/',status_code=status.HTTP_200_OK)
async def get_user(user:user_dependency, db:db_dependency):
    if user is None:
        raise HTTPException(status_code=401,detail='Authenticatio Failed')
    return db.query(Users).filter(Users.id == user.get('id')).first()


@router.put('/password', status_code=status.HTTP_204_NO_CONTENT)
async def change_password(user:user_dependency, db:db_dependency, user_verification : UserVerification): #user_verification is our response body.
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()
    
    if not bcrypt_context.verify(user_verification.password, user_model.hashed_password):
        raise HTTPException(status_code=401, detail='Error on password change')
    user_model.hashed_password = bcrypt_context.hash(user_verification.new_password)
    db.add(user_model)
    db.commit()
 
    
@router.put('/phonenumber/{phone_number}', status_code=status.HTTP_204_NO_CONTENT)
async def change_phone_number(user:user_dependency,db:db_dependency,phone_number:str):
    if user is None:
        raise HTTPException(status_code=401,detail='Authentication Failed')
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()
    user_model.phone_number = phone_number
    db.add(user_model)
    db.commit()
    
    
    
    
    
    
    

    
    
from fastapi import APIRouter,Depends,HTTPException,Path
from ..models import Todos
from ..database import SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from pydantic import BaseModel,Field
from starlette import status
from .auth import get_current_user

router = APIRouter(
    prefix='/admin',
    tags=['admin']
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


@router.get('/todo',status_code=status.HTTP_200_OK)
async def read_all(user:user_dependency, db:db_dependency):
    if user is None or user.get('user_role') != 'admin':
        raise HTTPException(status_code=401, detail='AUTHENTICATION FAILED')
    
    return db.query(Todos).all()

        
@router.delete('/todo/{todo_id}',status_code=status.HTTP_204_NO_CONTENT)
async def  delete_todo(user:user_dependency, db:db_dependency, todo_id:int = Path(gt=0)):
    if user is None or user.get('user_role') != 'admin':
        raise HTTPException(status_code=401, detail='Authentcation Failed')
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404,detail='Todo not found!')
    db.query(Todos).filter(Todos.id == todo_id).delete()
    db.commit()
        
    
    
from .utils import *
from ..routers.admin import get_current_user,get_db #we are importing this because we want to override our dependency injection with testing dependency.
from fastapi import status
from ..models import Todos

#Always make sure to override the dependencies of the file we are testing against.

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_admin_read_all_authenticated(test_todo):
    response = client.get('/admin/todo')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{'title' : 'Learn to code!', 'complete' : False, 'description' : 'Need to learn everyday','priority':5 ,'id':1, 'owner_id' : 1}]
    
    

def test_admin_delete(test_todo):
    response = client.delete('/todos/todo/1')
    assert response.status_code == 204
    
    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model is None
        
        

def test_delete_todo_not_found():
    response  = client.get('/todos/todo/999')
    assert response.status_code == 404
    assert response.json() == {'detail' : 'Todo not Found'}
    
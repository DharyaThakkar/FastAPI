from ..routers.todos import get_db,get_current_user
from fastapi import status
from .utils import *

#changing the dependencies for the testing purpose :-

app.dependency_overrides[get_db] = override_get_db #when we are calling get_db from test_todos, when want it to be override by the override_get_db.
app.dependency_overrides[get_current_user] = override_get_current_user
        

#Now we can write our test 

def test_read_all_authenticated(test_todo):
    response = client.get('/todos')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{'complete':False, 'title':'Learn to code!', 'description' : 'Need to learn everyday', 'id' : 1, 'priority' : 5, 'owner_id' : 1}]
    
# A pytest fixture is something which happens before the function is called.


def test_read_one_authenticated(test_todo):
    response = client.get('/todos/todo/1')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'complete':False, 'title':'Learn to code!', 'description' : 'Need to learn everyday', 'id' : 1, 'priority' : 5, 'owner_id' : 1}
    
    
    
def test_read_one_authenticated_not_found():
    response = client.get("/todos/todo/999")
    assert response.status_code == 404
    assert response.json() == {'detail' : 'Todo not Found'}
    
    
def test_create_todo(test_todo):
    request_data = {
        'title' : 'New Todo!',
        'description' : 'New todo description',
        'priority' : 5,
        'complete' : False
    }
    
    response = client.post('/todos/todo', json=request_data)
    assert response.status_code == 201 
    
    #we can even check more whether our todo is inside our database or not.
    #After saving the todo, we are also fetching it and confirming it whether the todo is saved perfectly or not.
    db = TestingSessionLocal() #creating a new database session to interact with it.
    model = db.query(Todos).filter(Todos.id == 2).first()
    assert model.title ==  request_data.get('title')
    assert model.description ==  request_data.get('description')
    assert model.complete == request_data.get('complete')
    assert model.priority == request_data.get('priority')
    

def test_update_todo(test_todo):
    request_data = {
        'title' : 'Change the title of the todo already saved!',
        'description' : 'Need to learn everyday',
        'priority' : 5,
        'complete' : False 
    }
    response = client.put('/todos/todo/1', json=request_data)
    assert response.status_code == 204
    
    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model.title == request_data.get('title')
    assert model.description == request_data.get('description')
    assert model.priority == request_data.get('priority')
    assert model.complete == request_data.get('complete')
    
    
def test_update_todo_not_found(test_todo):
    request_data = {
        'title' : 'Change the title of the todo already saved!',
        'description' : 'Need to learn everyday',
        'priority' : 5,
        'complete' : False 
    }
    response = client.put('/todos/todo/9999', json=request_data)
    assert response.status_code == 404 
    assert response.json() == {'detail' : 'Todo Not Found'} 
    
    
def test_delete_todo(test_todo):
    response = client.delete('/todos/todo/1')
    assert response.status_code == 204
    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model is None    
    
    
def test_delete_todo_not_found():
    response = client.delete('/todos/todo/999')
    assert response.status_code == 404
    assert response.json() == {'detail' : 'Todo Not Found'}
          
    

    
    
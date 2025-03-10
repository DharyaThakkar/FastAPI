from fastapi.testclient import TestClient #simple way of creating client for our app.
from ..main import app
from fastapi import status


client = TestClient(app)

def test_return_health_check():
    response = client.get("/healthy")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'status' : 'Healthy'}
    
    
    
    


 
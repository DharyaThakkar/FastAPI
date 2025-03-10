from fastapi import FastAPI,Request, status
from .models import Base
from .database import engine
from .routers import auth, todos, admin, users
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
app = FastAPI()

Base.metadata.create_all(bind=engine)#This will create verything from our database.py file and our models.py file.
#The above line of code will only run if our todos.db database does not exist.

# Base.metadata.create_all(bind=engine)


# templates = Jinja2Templates(directory='TodoApp/templates') #inside the templates directory we are going to have our HTML files.

app.mount("/static", StaticFiles(directory="TodoApp/static"), name='static')

@app.get('/')
def test(request:Request):
     return RedirectResponse(url="/todos/todo-page", status_code=status.HTTP_302_FOUND)




#creating a health-check route :-
@app.get("/healthy")
def health_check():
     return {'status' : 'Healthy'}
 
 
app.include_router(auth.router) #make sure to add the route of the auth.py module here in our main application.
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)



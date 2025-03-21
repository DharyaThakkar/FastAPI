from typing import Optional
from fastapi import FastAPI, Body, Path, Query, HTTPException
from pydantic import BaseModel, Field
from starlette import status

app = FastAPI()

class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_date: int 

    def __init__(self, id, title, author, description, rating, published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date
        
        
class BookRequest(BaseModel): #we will create a separate request model for data validation.
    #id: Optional[int] = None #This means that this field is null and it can be either of the type interger or of type None, which is also null.
    id: Optional[int] = Field(description='ID is not needed for create', default=None )
    title: str = Field(min_length = 3)
    author: str = Field(min_length = 1)
    description: str = Field(min_length = 1, max_length = 100)
    rating: int = Field(gt = 0, lt = 6)
    published_date: int = Field(gt=1999, lt=2031)
    
    #we can update the example schema like this :-
    model_config  = {
        "json_schema_extra": {
            "example": {
                "title":"A new book",
                "author": "Dharya Thakkar",
                "description": "A new description of a book",
                "rating" : 5,
                "published_date" : 2029
            }
        }
    }
        
BOOKS = [
    Book(1,'Computer Science Pro', 'codingwithroby', 'A very nice book!', 5, 2030),
    Book(2,'Be Fast with FastAPI', 'codingwithroby', 'A great book!', 5, 2030),
    Book(3,'Master Endpoints', 'codingwithroby', 'A Awesome book!', 5, 2029),
    Book(4,'HP1', 'Author 1', 'Book Description', 2, 2028),
    Book(5,'HP2', 'Author 2', 'Book Description', 3, 2027),
    Book(6,'HP3', 'Author 3', 'Book Description', 1, 2026)
]

@app.get("/books", status_code=status.HTTP_200_OK)#SO , here we are explicitly saying, after our read_all books is successful, we want to return the status code of 200.
async def read_all_books():
    return BOOKS



@app.get('/books/{book_id}', status_code=status.HTTP_200_OK)
async def read_book(book_id:int = Path(gt=0)): #so this is how we are applying validations to our path parame ters
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail='Item not found')#if the book the user is searching for cannot be found.
 
      
@app.get('/book/', status_code=status.HTTP_200_OK)
async def read_book_by_rating(book_rating:int = Query(gt=0, lt=6)):
    books_to_return = []
    for book in BOOKS:
        if book.rating == book_rating:
            books_to_return.append(book)
    return books_to_return  
    
    
@app.get('/books/published/',status_code=status.HTTP_200_OK)
async def read_book_by_published_date(published_date:int = Query(gt=1999, lt=2031)):
    books_to_return = []
    for book in BOOKS:
        if book.published_date == published_date:
            books_to_return.append(book)
    return books_to_return
    

# @app.post("/create-book")
# async def create_book(book_request = Body()):
#     BOOKS.append(book_request)

@app.post("/create-book",status_code=status.HTTP_201_CREATED)
async def create_book(book_request : BookRequest): #so whatever is in the body of this post request we are naming it as 'book_request' and converting it to a type 'Book_Request'.
    new_book = Book(**book_request.model_dump()) #All the validation will happen before we are converting the BookRequest object into the Book object.
    #print(type(new_book))
    BOOKS.append(find_book_id(new_book))
    
def find_book_id(book:Book):
        # if len(BOOKS) > 0:
        #     book.id = BOOKS[-1].id + 1
        # else:
        #     book.id = 1  
        #above code using ternary operation ->
        book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
        return book
    
@app.put("/books/update_book",status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book : BookRequest):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book
            book_changed=True
            
    if not book_changed:
        raise HTTPException(status_code=404, detail='Item not Found')
            
@app.delete('/books/{book_id}',status_code=status.HTTP_204_NO_CONTENT)#HERE ALSO WE ARE RETURNING A STATUS CODE OF 204, BECAUSE HERE ALSO WE ARE NOT CREATING AND NOR RETURNING ANYTHING, WE ARE JUST MODIFYING THE CONTENT.
async def delete_book(book_id:int = Path(gt=0)):
    book_deleted = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            book_deleted = True
            break 
    if not book_deleted:
        raise HTTPException(status_code=404, detail= 'book to be deleted is not found')
    
            
        
    
    
        
    
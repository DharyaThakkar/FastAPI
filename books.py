from fastapi import FastAPI,Body

app = FastAPI() #This allows Uvicorn to indentify that hey, we are creating a new application of fast API.Uvicorn is the web server we use to start a FastAPI application.

BOOKS = [
    {'title':'Title One', 'author': 'Author One', 'category': 'science'},
    {'title':'Title Two', 'author': 'Author Two', 'category': 'science'},
    {'title':'Title Three', 'author': 'Author Three', 'category': 'history'},
    {'title':'Title Four', 'author': 'Author Four', 'category': 'math'},
    {'title':'Title Five', 'author': 'Author Five', 'category': 'math'},
    {'title':'Title Six', 'author': 'Author Two', 'category': 'math'}
]

@app.get("/books") #Acknowleding that this is a API endpoint
async def read_all_books():
    return BOOKS #returning a dictionary
#async id fairly optional for FastAPI.


@app.get('/books/{book_title}')
async def read_book(book_title:str):
    for book in BOOKS:
        if book.get('title').casefold() == book_title.casefold(): #casefold() is more powerful way of saying lower-case.
            return book


# @app.get("/books/mybook")
# async def read_all_books():
#     return {'book_title' : 'My Favourite book'}

# #Path parameters :- Sending dynamic data through the api endpoint.its like providing the complete path of the data.

# @app.get('/books/{dynamic_param}') #This dynamic_param located inside this api-end point is going to match the parameter name of the function underneath.
# async def read_all_books(dynamic_param : str): #we are explicitly specifying the type of this dynamic_param.so, now if we paas any number as the value of the dynamic_param, it will be coverted into string.
#     return {"dynamic_param" : dynamic_param}

#query parameter is a way to filter data based on the url provided.it is a way of filtering our data based on certain conditions.And in path parameter we are not filtering out the data based on certain condition, we instead is directly getting the actual required data.This is the main difference between these two's.
@app.get('/books/')#with query parameter fast api automatically knows that, hey anything that is passed in after books, that is not a dynamic and is a query paramter, so for it we do not have to specify anything in the endpoint.
async def read_category_by_query(category:str):
    books_to_return = []
    for book in BOOKS:
        if book.get('category').casefold() == category.casefold():
            books_to_return.append(book)
    return books_to_return


#using both path and query parameters together :-
#endpoint which searches by the author and filter out using the category :-

#Assignment-1(Section-5)
#using query parameters

@app.get("/books/get_specific_book/")
async def get_specific_book(book_author:str):
    books = list([])#creating a empty list in a standard way.
    for i in range(len(BOOKS)):
        if BOOKS[i].get('author').casefold() == book_author.casefold():
            books.append(BOOKS[i])
    return books

@app.get('/books/{book_author}/')
async def read_author_category_by_query(book_author:str, category:str):
    books_to_return = []
    for book in BOOKS:
        if book.get('author').casefold() == book_author.casefold() and book.get('category').casefold() == category.casefold():
            books_to_return.append(book)
    return books_to_return



@app.post('/books/create_book')
async def create_book(new_book=Body()):
    BOOKS.append(new_book)
 
@app.put("/books/update_book")    
async def update_book(updated_book=Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == updated_book.get('title').casefold():
            BOOKS[i] = updated_book
 
            
@app.delete("/books/delete_book/{book_title}")
async def delete_book(book_title:str):#so now our path parameter will be converted into string, so we can now use it in our application.
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == book_title.casefold():
            BOOKS.pop(i)
            break
        
#Assignment-1(Section-5)

#using path parameters

# @app.get("/books/get_specific_book/{book_author}")
# async def get_specific_book(book_author:str):
#     books = list([])#creating a empty list in a standard way.
#     for i in range(len(BOOKS)):
#         if BOOKS[i].get('author').casefold() == book_author.casefold():
#             books.append(BOOKS[i])
#     return books   




       
    
            
    
        

    
    
    
    

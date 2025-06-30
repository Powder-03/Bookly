from fastapi import FastAPI , Header

app = FastAPI()

@app.get("/")
async def read_root():
    return {"Hello": "World"}


@app.get('/greet/{name}')
async def greet(name: str , age:int) -> dict: #example of path parameter and query parameter
    
    return {"Hello": name, "Age": age}

class BookCreateModel:
    title: str
    author: str
    

@app.post("/create_book")
async def create_book(book_data: BookCreateModel) :
    return {
        "title": book_data.title,
        "author": book_data.author
    }
    
@app.get("/get_headers")
async def get_headers(
    accept: str = Header(None),
    content_type: str = Header(None),
):
    request_headers = {}

    request_headers['Accept'] = accept
    
    return request_headers
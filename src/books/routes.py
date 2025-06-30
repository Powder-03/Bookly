from fastapi import APIRouter , status, HTTPException
from src.books.schemas import Book, BookCreateModel, BookUpdateModel
from src.books.book_data import books_db
from typing import List

book_router = APIRouter()


@book_router.get('/' , response_model=list[Book])
async def get_all_books():
    return books_db


@book_router.post('/', response_model=Book, status_code=201)
async def create_book(book_data: BookCreateModel) -> Book:
    new_book = book_data.model_dump()
    new_book["id"] = len(books_db) + 1
    books_db.append(new_book)
    return new_book



@book_router.get('/{book_id}', response_model=Book)
async def get_book_by_id(book_id: int):
    for book in books_db:
        if book["id"] == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")
    


@book_router.put('/{book_id}', response_model=Book)
async def update_book(book_id: int, book: BookUpdateModel):
    for i, b in enumerate(books_db):
        if b["id"] == book_id:
            # Convert Pydantic model to dict and merge with existing book
            book_data = book.model_dump()
            books_db[i] = {**b, **book_data}
            return books_db[i]
    raise HTTPException(status_code=404, detail="Book not found")


@book_router.delete('/{book_id}', status_code=200)
async def delete_book(book_id: int):
    for i, book in enumerate(books_db):
        if book["id"] == book_id:
            deleted_book = books_db.pop(i)
            return {"message": f"Book '{deleted_book['title']}' deleted successfully"}
    raise HTTPException(status_code=404, detail="Book not found")
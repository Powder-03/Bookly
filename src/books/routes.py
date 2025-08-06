from fastapi import APIRouter , status, HTTPException , Depends
from src.books.models import Book  # ← Fixed: Import Book from models, not schemas
from src.books.schemas import BookCreateModel, BookUpdateModel
from .service import BookService
from src.db.main import get_session
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List
import uuid
from src.auth.dependencies import AccessTokenBearer , RoleChecker


role_checker = Depends(RoleChecker(['admin' , 'user'])) # This allows only admin users to access certain endpoints

book_service = BookService()

book_router = APIRouter()
access_token_bearer = AccessTokenBearer()


@book_router.get('/' , response_model=list[Book] , dependencies=[role_checker])
async def get_all_books(session: AsyncSession = Depends(get_session), user_details=Depends(access_token_bearer)) -> List[Book]:
    return await book_service.get_all_books(session)


@book_router.post('/', response_model=Book, status_code=201 , dependencies=[role_checker])
async def create_book(book_data: BookCreateModel, session: AsyncSession = Depends(get_session), user_details = Depends(access_token_bearer)) -> Book:
    return await book_service.create_book(book_data, session)



@book_router.get('/{book_uid}', response_model=Book , dependencies=[role_checker])
async def get_book_by_id(book_uid: str, session: AsyncSession = Depends(get_session) , user_details = Depends(access_token_bearer)):
    book = await book_service.get_book(session, book_uid)
    if book:
        return book
    raise HTTPException(status_code=404, detail="Book not found")
    


@book_router.put('/{book_uid}', response_model=Book ,  dependencies=[role_checker])
async def update_book(book_uid: str, book_update: BookUpdateModel, session: AsyncSession = Depends(get_session) , user_details = Depends(access_token_bearer)):
    updated_book = await book_service.update_book(book_uid, book_update, session)
    if updated_book:
        return updated_book
    raise HTTPException(status_code=404, detail="Book not found")


@book_router.delete('/{book_uid}', status_code=200 , dependencies=[role_checker])
async def delete_book(book_uid: str, session: AsyncSession = Depends(get_session) , user_details = Depends(access_token_bearer)):
    deleted = await book_service.delete_book(book_uid, session)
    if deleted:
        return {"message": f"Book with UID {book_uid} deleted successfully"}
    raise HTTPException(status_code=404, detail="Book not found")  

# This router handles all book-related endpoints, including getting all books,
# creating a new book, getting a specific book by ID, updating a book, and deleting a book.
# It uses the BookService to interact with the database and perform the necessary operations.   
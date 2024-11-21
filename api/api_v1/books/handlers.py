from typing import Annotated

from fastapi import APIRouter, Depends, status

from core.settings import settings

from .dependencies import get_book_service
from .repository.dependencies import get_book_by_params
from .schemas import Book, BookCreate, BookUpdatePartial
from .service import BookService

router = APIRouter(
    prefix=settings.api.v1.books,
    tags=["books"],
)


@router.get("", response_model=list[Book], status_code=status.HTTP_200_OK)
async def get_books(service: Annotated[BookService, Depends(get_book_service)]):
    books = await service.get_books()
    return books


@router.get("/{book_id_or_title}", response_model=Book, status_code=status.HTTP_200_OK)
async def get_book_by_id(
    book: Annotated[Book, Depends(get_book_by_params)],
):
    return book


@router.post("", response_model=BookCreate, status_code=status.HTTP_201_CREATED)
async def create_book(
    book_in: BookCreate,
    service: Annotated[BookService, Depends(get_book_service)],
):
    new_book = await service.create_book(book_in=book_in)
    return new_book


@router.patch(
    "/{book_id_or_title}", response_model=BookUpdatePartial, status_code=status.HTTP_200_OK
)
async def update_book(
    book: Annotated[Book, Depends(get_book_by_params)],
    book_in: BookUpdatePartial,
    service: Annotated[BookService, Depends(get_book_service)],
):
    updated_book = await service.update_book(book=book, book_in=book_in)
    return updated_book


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book_by_id(
    book_id: int,
    service: Annotated[BookService, Depends(get_book_service)],
):
    await service.delete_book_by_id(book_id=book_id)

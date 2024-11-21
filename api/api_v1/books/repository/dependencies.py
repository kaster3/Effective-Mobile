from typing import Annotated

from fastapi import Depends, HTTPException, Path

from api.api_v1.books.dependencies import get_book_repository
from core.database.models import Book

from .books import BookRepository


async def get_book_by_params(
    book_params: Annotated[str, Path],
    repository: Annotated[BookRepository, Depends(get_book_repository)],
) -> Book:

    if book_params.isdigit():
        book = await repository.get_by_id(book_id=int(book_params))
    else:
        book = await repository.get_by_title(book_title=book_params)

    if book is not None:
        return book
    raise HTTPException(status_code=404, detail="Book not found")

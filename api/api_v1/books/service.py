import logging

from fastapi import HTTPException

from api.api_v1.books.repository.books import BookRepository
from api.api_v1.books.repository.cache_books import CacheRepository
from api.api_v1.books.schemas import Book as BookSchema
from api.api_v1.books.schemas import BookCreate, BookUpdatePartial
from core.database.models import Book

log = logging.getLogger(__name__)


class BookService:
    def __init__(self, repository: BookRepository, cache: CacheRepository):
        self.repository = repository
        self.cache = cache

    async def get_books(self) -> list[BookSchema]:
        if cache_books := await self.cache.get_books():
            log.debug("--------------------------------")
            return cache_books
        else:
            books = await self.repository.get_books()
            books_schema = [BookSchema.model_validate(book) for book in books]
            await self.cache.set_books(books_schema)
            return books_schema

    async def create_book(self, book_in: BookCreate) -> Book:
        # Проверяем нет ли уже книги с таким названием так как полу уникально
        if await self.repository.get_by_title(book_in.title):
            raise HTTPException(status_code=400, detail="Book with this title already exists")

        new_book = await self.repository.create_book(book_in=book_in)
        return new_book

    async def update_book(self, book: Book, book_in: BookUpdatePartial) -> Book:
        # Проверяем нет ли уже книги с таким названием так как полу уникально
        if book_in.title and await self.repository.get_by_title(book_in.title):
            raise HTTPException(status_code=400, detail="Book with this title already exists")

        updated_book = await self.repository.update_book(book=book, book_in=book_in)
        return updated_book

    async def delete_book_by_id(self, book_id: int) -> None:
        book = await self.repository.get_by_id(book_id=book_id)
        await self.repository.delete_book(book=book)

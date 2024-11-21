import sqlalchemy
from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.books.schemas import BookCreate, BookUpdatePartial
from core.database.models import Book


class BookRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_books(self) -> list[Book]:
        smtp = select(Book).order_by(Book.id)
        books = await self.session.scalars(smtp)
        return list(books)

    async def get_by_id(self, book_id: int) -> Book | None:
        book = await self.session.get(Book, book_id)
        return book

    async def get_by_title(self, book_title: str) -> Book | None:
        smtp = select(Book).where(Book.title == book_title)
        book = await self.session.scalar(smtp)
        return book

    async def create_book(self, book_in: BookCreate) -> Book:
        book = Book(**book_in.model_dump())
        self.session.add(book)
        await self.session.commit()
        await self.session.refresh(book)
        return book

    async def update_book(
        self,
        book: Book,
        book_in: BookUpdatePartial,
    ) -> Book:
        for key, value in book_in.model_dump(exclude_unset=True).items():
            setattr(book, key, value)
        await self.session.commit()
        return book

    async def delete_book(self, book: Book) -> None:
        try:
            await self.session.delete(book)
            await self.session.commit()
        except sqlalchemy.exc.IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Cannot delete category"
            )

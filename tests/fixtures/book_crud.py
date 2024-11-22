import pytest_asyncio
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from core.database.models import Book


@pytest_asyncio.fixture()
async def create_books(db_session: AsyncSession):
    async with db_session.begin():
        smtp = text("""
            INSERT INTO books (title, author, year, status)
            VALUES ('Test title 1', 'Test author 1', 1000, 'IN_STOCK'),
                   ('Test title 2', 'Test author 2', 1000, 'CHECKED_OUT');
            """)
        await db_session.execute(smtp)
        await db_session.commit()


@pytest_asyncio.fixture()
async def get_book_by_id(db_session: AsyncSession, create_books) -> Book | None:
    book = await db_session.get(Book, 1)
    return book
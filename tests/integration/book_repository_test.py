import pytest
from syrupy import SnapshotAssertion, snapshot

from api.api_v1.books.schemas import BookCreate, BookUpdatePartial
from core.database.models import Book
from api.api_v1.books.repository.books import BookRepository
from core.database.models.books import BookStatus


@pytest.mark.asyncio
async def test_get_all_books(init_models, create_books, book_repository: BookRepository, snapshot: SnapshotAssertion):
    books = await book_repository.get_books()
    assert len(books) == 2
    assert isinstance(books[0], Book)
    assert isinstance(books[1], Book)

    snapshot.assert_match([book.to_dict() for book in books])


@pytest.mark.asyncio
async def test_create_book(init_models, book_repository: BookRepository, snapshot: SnapshotAssertion):
    book_1 = await book_repository.create_book(
        BookCreate(title="Test title 1", author="Test author 1", year=1000, status=BookStatus.IN_STOCK)
    )
    book_2 = await book_repository.create_book(
        BookCreate(title="Test title 2", author="Test author 1", year=1000, status=BookStatus.CHECKED_OUT)
    )

    snapshot.assert_match(book_1.to_dict())
    snapshot.assert_match(book_2.to_dict())



@pytest.mark.asyncio
async def test_get_book_by_id(init_models, create_books, book_repository: BookRepository, snapshot: SnapshotAssertion):
    book_1 = await book_repository.get_by_id(1)
    book_2 = await book_repository.get_by_id(2)
    book_3 = await book_repository.get_by_id(3)

    assert book_1 is not None
    assert book_2 is not None
    assert book_3 is None

    snapshot.assert_match(book_1.to_dict())
    snapshot.assert_match(book_2.to_dict())

@pytest.mark.asyncio
async def test_get_book_by_title(init_models, create_books, book_repository: BookRepository, snapshot: SnapshotAssertion):
    book_1 = await book_repository.get_by_title(book_title="Test title 1")
    book_2 = await book_repository.get_by_title(book_title="Test title 2")
    book_3 = await book_repository.get_by_title(book_title="Test title 3")

    assert book_1 is not None
    assert book_2 is not None
    assert book_3 is None

    snapshot.assert_match(book_1.to_dict())
    snapshot.assert_match(book_2.to_dict())


@pytest.mark.asyncio
async def test_update_book(init_models, get_book_by_id: Book, book_repository: BookRepository, snapshot: SnapshotAssertion):
    assert get_book_by_id is not None
    snapshot.assert_match(get_book_by_id.to_dict())

    updated_book = await book_repository.update_book(
        book=get_book_by_id,
        book_in=BookUpdatePartial(
            title="Updated title",
            author="Updated author",
            year=2000,
            status=BookStatus.CHECKED_OUT)
    )

    snapshot.assert_match(updated_book.to_dict())



@pytest.mark.asyncio
async def test_delete_book(init_models, get_book_by_id: Book, book_repository: BookRepository):
    assert get_book_by_id is not None
    assert isinstance(get_book_by_id, Book)
    await book_repository.delete_book(book=get_book_by_id)
    book = await book_repository.get_by_id(get_book_by_id.id)
    assert book is None





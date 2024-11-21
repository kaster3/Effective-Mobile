from pydantic import BaseModel, ConfigDict

from core.database.models.books import BookStatus


class BaseBook(BaseModel):
    title: str
    author: str
    year: int
    status: BookStatus


class Book(BaseBook):
    model_config = ConfigDict(from_attributes=True)
    id: int


class BookCreate(BaseBook):
    pass


class BookUpdate(BaseBook):
    pass


class BookUpdatePartial(BaseBook):
    title: str | None = None
    author: str | None = None
    year: int | None = None
    status: BookStatus | None = None

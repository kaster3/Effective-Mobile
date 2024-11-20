from enum import Enum

from sqlalchemy import Enum as SQLEnum
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from core.database.models.base import Base
from core.database.models.mixins import IntIdPkMixin


class BookStatus(Enum):
    IN_STOCK = "В наличие"
    CHECKED_OUT = "Выдана"


class Book(Base, IntIdPkMixin):
    title: Mapped[str] = mapped_column(String(30), unique=True)
    author: Mapped[str] = mapped_column(String(30))
    year: Mapped[int] = mapped_column(Integer)
    status: Mapped[BookStatus] = mapped_column(SQLEnum(BookStatus))

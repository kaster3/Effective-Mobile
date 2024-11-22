from typing import Annotated

from fastapi import Depends
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from api.api_v1.books.repository.books import BookRepository
from api.api_v1.books.repository.cache_books import CacheRepository
from api.api_v1.books.service import BookService
from core.database.db_helper import db_helper
from core.settings import Settings


async def get_settings() -> Settings:
    return Settings()


async def get_book_repository(
    session: AsyncSession = Depends(db_helper.session_getter),
) -> BookRepository:
    return BookRepository(session=session)


async def get_redis_connection(settings: Settings) -> Redis:
    return await Redis(
        host=settings.redis.host, port=settings.redis.port, db=settings.redis.db
    )


async def get_cache_repository() -> CacheRepository:
    redis_connection = await get_redis_connection(settings=await get_settings())
    return CacheRepository(redis_connection)


async def get_book_service(
    repository: BookRepository = Depends(get_book_repository),
    cache_repository: CacheRepository = Depends(get_cache_repository),
) -> BookService:
    return BookService(repository=repository, cache=cache_repository)

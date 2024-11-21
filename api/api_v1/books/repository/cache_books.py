import json

from redis import asyncio as Redis

from api.api_v1.books.schemas import Book


class CacheRepository:
    def __init__(self, redis: Redis):
        self.redis = redis

    async def get_books(self) -> list[Book]:
        async with self.redis as redis:
            books_json = await redis.lrange("books", 0, -1)

            return [Book.model_validate(json.loads(book)) for book in books_json]

    async def set_books(self, books: list[Book]):
        books_json = [book.json() for book in books]
        async with self.redis as redis:
            await redis.lpush("books", *books_json)

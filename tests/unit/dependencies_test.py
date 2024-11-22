from unittest.mock import MagicMock, patch

import pytest
from redis.asyncio import Redis
from syrupy import snapshot

from api.api_v1.books.dependencies import (
    get_book_repository,
    get_book_service,
    get_cache_repository,
    get_redis_connection,
    get_settings,
)
from api.api_v1.books.repository.books import BookRepository
from api.api_v1.books.repository.cache_books import CacheRepository
from api.api_v1.books.service import BookService
from core.settings import RedisConfig, Settings


@pytest.mark.asyncio
async def test_get_book_repository():
    book_repository = await get_book_repository()
    assert book_repository is not None
    assert isinstance(book_repository, BookRepository)


@pytest.mark.asyncio
async def test_get_cache_repository():
    cache_repository = await get_cache_repository()
    assert cache_repository is not None
    assert isinstance(cache_repository, CacheRepository)


@pytest.mark.asyncio
async def test_get_book_service(book_repository: BookRepository):
    book_service = await get_book_service(repository=book_repository)
    assert book_service is not None
    assert isinstance(book_service, BookService)


@pytest.mark.asyncio
async def test_get_redis_connection():
    mock_redis_config = MagicMock(spec=RedisConfig)
    mock_redis_config.url = "redis://localhost:6379/0"
    mock_redis_config.host = "localhost"
    mock_redis_config.port = 6379
    mock_redis_config.db = 0

    mock_settings_instance = MagicMock(spec=Settings)
    mock_settings_instance.redis = mock_redis_config

    with patch("core.settings.settings", new=mock_settings_instance):
        redis_connection = await get_redis_connection(settings=mock_settings_instance)

        assert redis_connection is not None
        assert isinstance(redis_connection, Redis)

        connection_kwargs = redis_connection.connection_pool.connection_kwargs
        assert connection_kwargs["host"] == "localhost"
        assert connection_kwargs["port"] == 6379
        assert connection_kwargs["db"] == 0


@pytest.mark.asyncio
async def test_get_settings(snapshot):
    settings = await get_settings()
    assert settings is not None
    assert isinstance(settings, Settings)

    snapshot.assert_match(settings)

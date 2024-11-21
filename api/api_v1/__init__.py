from fastapi import APIRouter

from core import settings

from .books.handlers import router as book_router

router = APIRouter(
    prefix=settings.api.v1.prefix,
)

for rout in (book_router,):
    router.include_router(
        router=rout,
    )


@router.get("")
async def root():
    return {"message": "this path is http://127.0.0.1:8000/api/v1"}

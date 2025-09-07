from contextlib import asynccontextmanager
from typing import AsyncIterator

import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from redis import asyncio as aioredis

from src.core.config import settings
from src.utils import db_helper

from api_v1 import router as api_v1_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    redis = aioredis.from_url(
        f"redis://{settings.redis_config.hostname}:{settings.redis_config.port}"
    )
    FastAPICache.init(RedisBackend(redis), prefix=settings.redis_config.prefix)
    yield
    await db_helper.dispose()


app = FastAPI(title="Bookly", default_response_class=ORJSONResponse, lifespan=lifespan)

app.include_router(api_v1_router)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)

import asyncio
from contextlib import asynccontextmanager
from typing import AsyncIterator

import uvicorn
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from prometheus_fastapi_instrumentator import Instrumentator

from redis import asyncio as aioredis
from slowapi import Limiter
from slowapi.util import get_remote_address

from src.core.config import settings
from src.middleware.register_middleware import register_middleware
from src.utils import db_helper

from api_v1 import router as api_v1_router
from src.utils.clean_reset_token import clean_password_reset_tokens_table
from src.utils.clean_verification_token import clean_email_verification_tokens_table


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    redis = aioredis.from_url(
        f"redis://{settings.redis_config.hostname}:{settings.redis_config.port}"
    )
    FastAPICache.init(RedisBackend(redis), prefix=settings.redis_config.prefix)
    asyncio.create_task(clean_email_verification_tokens_table())
    asyncio.create_task(clean_password_reset_tokens_table())
    yield
    await db_helper.dispose()


app = FastAPI(title="Bookly", default_response_class=ORJSONResponse, lifespan=lifespan)

limiter = Limiter(key_func=get_remote_address, default_limits=["20/minute"])

instrumentator = Instrumentator(should_group_status_codes=False,
                                excluded_handlers=["/metrics"])

instrumentator.instrument(app).expose(app)

app.state.limiter = limiter

register_middleware(app=app)

app.include_router(api_v1_router)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)

from fastapi import APIRouter
from src.api_v1.user.views import router as users_router
from src.api_v1.profile.views import router as profiles_router
from src.api_v1.book.views import router as books_router
from src.api_v1.author.views import router as authors_router
from src.api_v1.review.views import router as reviews_router

router = APIRouter(prefix="/api_v1")

router.include_router(users_router)

router.include_router(profiles_router)

router.include_router(books_router)

router.include_router(authors_router)

router.include_router(reviews_router)
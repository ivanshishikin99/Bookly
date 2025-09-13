from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.api_v1.review.crud import create_review
from src.api_v1.review.dependencies import get_review_by_id_dependency
from src.api_v1.review.schemas import ReviewRead, ReviewCreate
from src.core.models import User, Review
from src.utils import db_helper
from src.utils.auth_helpers import get_user_by_token

router = APIRouter(prefix="/review", tags=["Reviews"])


@router.post("/{book_id}", response_model=ReviewRead, status_code=status.HTTP_200_OK)
async def create_review_view(book_id: int,
                             review_data: ReviewCreate,
                             user: User = Depends(get_user_by_token),
                             session: AsyncSession = Depends(db_helper.session_getter)) -> Review | HTTPException:
    return await create_review(book_id=book_id, user=user,
                               review_data=review_data, session=session)


@router.get("/{review_id}", response_model=ReviewRead, status_code=status.HTTP_200_OK)
async def get_review_by_id_view(review: Review = Depends(get_review_by_id_dependency)) -> Review | HTTPException:
    return review


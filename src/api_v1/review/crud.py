from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api_v1.review.schemas import ReviewCreate
from src.core.models import User, Review


async def create_review(book_id: int,
                        user: User,
                        review_data: ReviewCreate,
                        session: AsyncSession) -> Review | HTTPException:
    if not user.verified:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Please, verify your e-mail to leave reviews.")
    review = Review(book_id=book_id,
                    user_id=user.id,
                    title=review_data.title,
                    text=review_data.text)
    session.add(review)
    await session.commit()
    return review


async def get_review_by_id(review_id: int,
                           session: AsyncSession) -> Review | HTTPException:
    try:
        review = await session.get(Review, review_id)
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review not found.")
    return review
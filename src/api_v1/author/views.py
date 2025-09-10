from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.api_v1.author.crud import create_author, update_author_partial, update_author_full, delete_author
from src.api_v1.author.dependencies import get_author_by_id_dependency
from src.api_v1.author.schemas import AuthorRead, AuthorCreate, AuthorUpdatePartial, AuthorUpdateFull
from src.core.models import User, Author
from src.utils import db_helper
from src.utils.auth_helpers import get_user_by_token

router = APIRouter(prefix="/author", tags=["Authors"])


@router.post("/", response_model=AuthorRead, status_code=status.HTTP_201_CREATED)
async def create_author_view(author_data: AuthorCreate,
                             user: User = Depends(get_user_by_token),
                             session: AsyncSession = Depends(db_helper.session_getter)) -> Author | HTTPException:
    return await create_author(author_data=author_data,
                               user=user,
                               session=session)


@router.get("/{author_id}", response_model=AuthorRead, status_code=status.HTTP_200_OK)
async def get_author_by_id_view(author: Author = Depends(get_author_by_id_dependency)) -> Author | HTTPException:
    return author


@router.patch("/{author_id}", response_model=AuthorRead, status_code=status.HTTP_200_OK)
async def update_author_partial_view(author_data: AuthorUpdatePartial,
                                     author: Author = Depends(get_author_by_id_dependency),
                                     user: User = Depends(get_user_by_token),
                                     session: AsyncSession = Depends(db_helper.session_getter)) -> Author | HTTPException:
    return await update_author_partial(author_data=author_data,
                                       author=author,
                                       user=user,
                                       session=session)


@router.put("/{author_id}", response_model=AuthorRead, status_code=status.HTTP_200_OK)
async def update_author_full_view(author_data: AuthorUpdateFull,
                                  author: Author = Depends(get_author_by_id_dependency),
                                  user: User = Depends(get_user_by_token),
                                  session: AsyncSession = Depends(db_helper.session_getter)) -> Author | HTTPException:
    return await update_author_full(author_data=author_data,
                                    author=author,
                                    user=user,
                                    session=session)


@router.delete("{author_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_author_view(author: Author = Depends(get_author_by_id_dependency),
                             user: User = Depends(get_user_by_token),
                             session: AsyncSession = Depends(db_helper.session_getter)):
    return await delete_author(author=author,
                               user=user,
                               session=session)



from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.api_v1.genre.crud import create_genre, delete_genre, update_genre_partial, update_genre_full
from src.api_v1.genre.dependencies import get_genre_by_id_dependency
from src.api_v1.genre.schemas import GenreRead, GenreCreate, GenreUpdatePartial, GenreUpdateFull
from src.core.models import User, Genre
from src.utils import db_helper
from src.utils.auth_helpers import get_user_by_token

router = APIRouter(prefix="/genre", tags=["Genres"])


@router.post("/", response_model=GenreRead, status_code=status.HTTP_200_OK)
async def create_genre_view(genre_data: GenreCreate,
                            user: User = Depends(get_user_by_token),
                            session: AsyncSession = Depends(db_helper.session_getter)) -> Genre | HTTPException:
    return await create_genre(genre_data=genre_data,
                              user=user,
                              session=session)


@router.get("/{genre_id}", response_model=GenreRead, status_code=status.HTTP_200_OK)
async def get_genre_by_id_view(genre: Genre = Depends(get_genre_by_id_dependency)) -> Genre | HTTPException:
    return genre


@router.delete("{genre_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_genre_view(genre: Genre = Depends(get_genre_by_id_dependency),
                            session: AsyncSession = Depends(db_helper.session_getter)):
    return await delete_genre(genre=genre,
                              session=session)


@router.patch("{genre_id}", response_model=GenreRead, status_code=status.HTTP_200_OK)
async def update_genre_partial_view(genre_data: GenreUpdatePartial,
                                    genre: Genre = Depends(get_genre_by_id_view),
                                    user: User = Depends(get_user_by_token),
                                    session: AsyncSession = Depends(db_helper.session_getter)) -> Genre | HTTPException:
    return await update_genre_partial(genre_data=genre_data,
                                      genre=genre,
                                      user=user,
                                      session=session)


@router.put("/{genre_id}", response_model=GenreRead, status_code=status.HTTP_200_OK)
async def update_genre_full_view(genre_data: GenreUpdateFull,
                                 genre: Genre = Depends(get_genre_by_id_dependency),
                                 user: User = Depends(get_user_by_token),
                                 session: AsyncSession = Depends(db_helper.session_getter)) -> Genre | HTTPException:
    return await update_genre_full(genre_data=genre_data,
                                   genre=genre,
                                   user=user,
                                   session=session)
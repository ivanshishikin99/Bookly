from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api_v1.genre.schemas import GenreCreate, GenreUpdatePartial, GenreUpdateFull
from src.core.models import User, Genre


async def create_genre(genre_data: GenreCreate,
                       user: User,
                       session: AsyncSession) -> Genre | HTTPException:
    if not user.role_access == "Super user":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only super users are allowed to add genres.")
    genre = Genre(**genre_data.model_dump())
    session.add(genre)
    await session.commit()
    return genre


async def get_genre_by_id(genre_id: int,
                          session: AsyncSession) -> Genre | None:
    return await session.get(Genre, genre_id)


async def delete_genre(genre: Genre,
                       session: AsyncSession):
    await session.delete(genre)
    await session.commit()
    return {"Genre deleted successfully."}


async def update_genre_partial(genre: Genre,
                               user: User,
                               genre_data: GenreUpdatePartial,
                               session: AsyncSession) -> Genre | HTTPException:
    if not user.role_access == "Super user":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only super users are allowed to modify genres.")
    for k, v in genre_data.model_dump().items():
        if k:
            setattr(genre, k, v)
    await session.commit()
    return genre


async def update_genre_full(genre: Genre,
                            user: User,
                            genre_data: GenreUpdateFull,
                            session: AsyncSession) -> Genre | HTTPException:
    if not user.role_access == "Super user":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only super users are allowed to add genres.")
    for k, v in genre_data.model_dump().items():
        setattr(genre, k, v)
    await session.commit()
    return genre
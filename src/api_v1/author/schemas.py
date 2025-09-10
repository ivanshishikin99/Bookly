from datetime import date

from pydantic import BaseModel


class AuthorCreate(BaseModel):
    full_name: str
    date_of_birth: date
    date_of_death: date | None
    bio: str


class AuthorRead(AuthorCreate):
    pass


class AuthorUpdateFull(AuthorCreate):
    pass


class AuthorUpdatePartial(BaseModel):
    full_name: str | None
    date_of_birth: date | None
    date_of_death: date | None
    bio: str | None
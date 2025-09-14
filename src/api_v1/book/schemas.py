from pydantic import BaseModel


class BookCreate(BaseModel):
    title: str
    year_of_release: int
    author_id: int
    genres: str
    description: str


class BookRead(BaseModel):
    title: str
    year_of_release: int
    author: str
    genres: str
    description: str


class BookUpdatePartial(BaseModel):
    title: str | None
    year_of_release: int | None
    author_id: int | None
    genres: str | None
    description: str | None


class BookUpdateFull(BookCreate):
    pass

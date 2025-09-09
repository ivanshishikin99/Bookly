from pydantic import BaseModel


class BookCreate(BaseModel):
    title: str
    year_of_release: int
    author: str
    description: str


class BookRead(BookCreate):
    pass


class BookUpdatePartial(BaseModel):
    title: str | None
    year_of_release: int | None
    author: str | None
    description: str | None


class BookUpdateFull(BookCreate):
    pass

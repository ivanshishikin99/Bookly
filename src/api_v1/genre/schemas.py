from pydantic import BaseModel


class GenreCreate(BaseModel):
    name: str


class GenreRead(GenreCreate):
    pass


class GenreUpdatePartial(GenreCreate):
    pass


class GenreUpdateFull(GenreCreate):
    pass

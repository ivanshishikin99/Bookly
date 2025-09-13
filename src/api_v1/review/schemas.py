from pydantic import BaseModel


class ReviewCreate(BaseModel):
    title: str
    text: str


class ReviewRead(ReviewCreate):
    pass


class ReviewUpdatePartial(BaseModel):
    title: str | None = None
    text: str | None = None


class ReviewUpdateFull(ReviewCreate):
    pass

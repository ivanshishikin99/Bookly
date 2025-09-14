from sqlalchemy import Table, Column, ForeignKey

from src.core.models import Base

BookGenreAssociationTable = Table(
    "book_genre_association_table",
    Base.metadata,
    Column("book_id", ForeignKey("book.id"), primary_key=True),
    Column("genre_id", ForeignKey("genre.id"), primary_key=True),
)
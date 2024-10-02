from app.db import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Integer
from uuid import UUID

class books(Base):
    __tablename__ = "books"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    year_published: Mapped[int] = mapped_column(Integer)
    title: Mapped[str] = mapped_column(String)
    author: Mapped[str] = mapped_column(String)
    genre: Mapped[str] = mapped_column(String)
    summary: Mapped[str] = mapped_column(String)

class reviews(Base):
    __tablename__ = "reviews"
    id: Mapped[str] = mapped_column(String, primary_key=True)
    book_id: Mapped[str] = mapped_column(String)
    user_id: Mapped[int] = mapped_column(Integer)
    rating: Mapped[int] = mapped_column(Integer)
    review_text: Mapped[str] = mapped_column(String)

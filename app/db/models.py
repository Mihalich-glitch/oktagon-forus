from sqlalchemy import String, Numeric, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .db import Base

class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)

    # Связь с книгами (одна категория -> много книг)
    books: Mapped[list["Book"]] = relationship(back_populates="category")

class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    url: Mapped[str] = mapped_column(String(500), default="")

    # Внешний ключ на таблицу категорий
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))

    # Ссылка на объект категории
    category: Mapped["Category"] = relationship(back_populates="books")
from sqlalchemy.orm import Session
from sqlalchemy import select
from .models import Book, Category

# --- Книги ---
def create_book(db: Session, title: str, price: float, category_id: int, **kwargs):
    new_book = Book(title=title, price=price, category_id=category_id, **kwargs)
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book

def get_all_books(db: Session):
    return db.scalars(select(Book)).all()

# --- Категории ---
def create_category(db: Session, title: str):
    new_cat = Category(title=title)
    db.add(new_cat)
    db.commit()
    db.refresh(new_cat)
    return new_cat

def get_all_categories(db: Session):
    return db.scalars(select(Category)).all()
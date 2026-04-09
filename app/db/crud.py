from sqlalchemy.orm import Session
from sqlalchemy import select
from . import models 
from .. import schemas

# --- Категории ---
def create_category(db: Session, category: schemas.CategoryCreate):
    new_cat = models.Category(**category.model_dump())
    db.add(new_cat)
    db.commit()
    db.refresh(new_cat)
    return new_cat

def get_categories(db: Session):
    return db.scalars(select(models.Category)).all()

def update_category(db: Session, category_id: int, category_update: schemas.CategoryCreate):
    db_cat = db.get(models.Category, category_id)
    if db_cat:
        for key, value in category_update.model_dump().items():
            setattr(db_cat, key, value)
        db.commit()
        db.refresh(db_cat)
    return db_cat


def delete_category(db: Session, category_id: int):
    db_category = db.get(models.Category, category_id)
    if db_category:
        db.delete(db_category)
        db.commit()
        return True
    return False

# --- Книги ---
def create_book(db: Session, book: schemas.BookCreate):
    new_book = models.Book(**book.model_dump())
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book

def get_all_books(db: Session):
    return db.scalars(select(models.Book)).all()

def update_book(db: Session, book_id: int, book_update: schemas.BookCreate):
    db_book = db.get(models.Book, book_id)
    if db_book:
        for key, value in book_update.model_dump().items():
            setattr(db_book, key, value)
        db.commit()
        db.refresh(db_book)
    return db_book

def delete_book(db: Session, book_id: int):
    db_book = db.get(models.Book, book_id)
    if db_book:
        db.delete(db_book)
        db.commit()
        return True
    return False


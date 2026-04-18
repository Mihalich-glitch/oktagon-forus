from sqlalchemy.orm import Session
from sqlalchemy import select
from . import models 
from .. import schemas

# --- Категории ---
def get_category(db: Session, category_id: int):
    return db.get(models.Category, category_id)

def get_categories(db: Session):
    return db.scalars(select(models.Category)).all()

def create_category(db: Session, category: schemas.CategoryCreate):
    db_category = models.Category(**category.model_dump())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def update_category(db: Session, db_category: models.Category, category_update: schemas.CategoryCreate):
    for key, value in category_update.model_dump().items():
        setattr(db_category, key, value)
    db.commit()
    db.refresh(db_category)
    return db_category

def delete_category(db: Session, db_category: models.Category):
    db.delete(db_category)
    db.commit()


# --- КНИГИ ---

def get_book(db: Session, book_id: int):
    return db.get(models.Book, book_id)

def get_books(db: Session, category_id: int = None):
    query = select(models.Book)
    if category_id:
        query = query.where(models.Book.category_id == category_id)
    return db.scalars(query).all()

def create_book(db: Session, book: schemas.BookCreate):
    db_book = models.Book(**book.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def update_book(db: Session, db_book: models.Book, book_update: schemas.BookCreate):
    for key, value in book_update.model_dump().items():
        setattr(db_book, key, value)
    db.commit()
    db.refresh(db_book)
    return db_book

def delete_book(db: Session, db_book: models.Book):
    db.delete(db_book)
    db.commit()


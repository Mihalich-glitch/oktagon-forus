from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import select
from typing import List, Optional

from ..db import crud, models, db
from .. import schemas

router = APIRouter(
    prefix="/books",
    tags=["books"]
)

# Зависимость для сессии БД
def get_db():
    database = db.SessionLocal()
    try:
        yield database
    finally:
        database.close()

@router.get("/", response_model=List[schemas.Book])
def read_books(category_id: Optional[int] = None, database: Session = Depends(get_db)):
    # Вся логика фильтрации теперь внутри crud.get_books
    return crud.get_books(database, category_id=category_id)

@router.post("/", response_model=schemas.Book, status_code=status.HTTP_201_CREATED)
def create_book(book: schemas.BookCreate, database: Session = Depends(get_db)):
    # Валидация бизнес-логики остается в роутере (это его работа)
    if not crud.get_category(database, book.category_id):
        raise HTTPException(status_code=400, detail="Category not found")
    return crud.create_book(database, book)

@router.put("/{book_id}", response_model=schemas.Book)
def update_book(book_id: int, book_update: schemas.BookCreate, database: Session = Depends(get_db)):
    db_book = crud.get_book(database, book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    if not crud.get_category(database, book_update.category_id):
        raise HTTPException(status_code=400, detail="Target category not found")
        
    return crud.update_book(database, db_book, book_update)
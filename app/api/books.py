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

# 1. Список книг с фильтрацией по категории
@router.get("/", response_model=List[schemas.Book])
def read_books(
    category_id: Optional[int] = Query(None, description="Фильтр по ID категории"),
    database: Session = Depends(get_db)
):
    query = select(models.Book)
    if category_id:
        # Добавляем фильтр в SQL запрос, если параметр передан
        query = query.where(models.Book.category_id == category_id)
    
    books = database.scalars(query).all()
    return books

# 2. Получить книгу по ID
@router.get("/{book_id}", response_model=schemas.Book)
def read_book(book_id: int, database: Session = Depends(get_db)):
    db_book = database.get(models.Book, book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book

# 3. Создать книгу (с валидацией категории)
@router.post("/", response_model=schemas.Book, status_code=status.HTTP_201_CREATED)
def create_book(book: schemas.BookCreate, database: Session = Depends(get_db)):
    # БИЗНЕС-ЛОГИКА: Проверяем, существует ли категория
    db_category = database.get(models.Category, book.category_id)
    if not db_category:
        raise HTTPException(
            status_code=400, 
            detail=f"Category with id {book.category_id} does not exist"
        )
    return crud.create_book(database, book)

# 4. Обновить книгу (с валидацией категории)
@router.put("/{book_id}", response_model=schemas.Book)
def update_book(book_id: int, book_update: schemas.BookCreate, database: Session = Depends(get_db)):
    db_book = database.get(models.Book, book_id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    # Если при обновлении меняется категория — проверяем её наличие
    db_category = database.get(models.Category, book_update.category_id)
    if not db_category:
        raise HTTPException(status_code=400, detail="Target category not found")

    for key, value in book_update.model_dump().items():
        setattr(db_book, key, value)
    
    database.commit()
    database.refresh(db_book)
    return db_book

# 5. Удалить книгу
@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int, database: Session = Depends(get_db)):
    success = crud.delete_book(database, book_id)
    if not success:
        raise HTTPException(status_code=404, detail="Book not found")
    return None
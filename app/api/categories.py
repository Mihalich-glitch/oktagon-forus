from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..db import crud, db, models
from .. import schemas 

router = APIRouter(
    prefix="/categories",
    tags=["categories"]
)

# Зависимость для получения сессии БД на каждый запрос
def get_db():
    database = db.SessionLocal()
    try:
        yield database
    finally:
        database.close()

# 1. Получить список всех категорий
@router.get("/", response_model=List[schemas.Category])
def read_categories(skip: int = 0, limit: int = 100, database: Session = Depends(get_db)):
    categories = crud.get_categories(database)
    return categories

# 2. Получить категорию по ID
@router.get("/{category_id}", response_model=schemas.Category)
def read_category(category_id: int, database: Session = Depends(get_db)):
    db_category = database.get(models.Category, category_id)
    if db_category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category

# 3. Создать категорию (Status 201 Created)
@router.post("/", response_model=schemas.Category, status_code=status.HTTP_201_CREATED)
def create_category(category: schemas.CategoryCreate, database: Session = Depends(get_db)):
    return crud.create_category(database, category)

# 4. Обновить категорию
@router.put("/{category_id}", response_model=schemas.Category)
def update_category(category_id: int, category: schemas.CategoryCreate, database: Session = Depends(get_db)):
    db_category = database.get(db.models.Category, category_id)
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    for key, value in category.model_dump().items():
        setattr(db_category, key, value)
    
    database.commit()
    database.refresh(db_category)
    return db_category

# 5. Удалить категорию
@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: int, database: Session = Depends(get_db)):
    success = crud.delete_category(database, category_id)
    if not success:
        raise HTTPException(status_code=404, detail="Category not found")
    return None # При 204 контент не возвращается
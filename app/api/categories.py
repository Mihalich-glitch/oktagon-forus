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

@router.get("/{category_id}", response_model=schemas.Category)
def read_category(category_id: int, database: Session = Depends(get_db)):
    db_category = crud.get_category(database, category_id)
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category

@router.put("/{category_id}", response_model=schemas.Category)
def update_category(category_id: int, category: schemas.CategoryCreate, database: Session = Depends(get_db)):
    db_category = crud.get_category(database, category_id)
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    return crud.update_category(database, db_category, category)

@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: int, database: Session = Depends(get_db)):
    db_category = crud.get_category(database, category_id)
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    crud.delete_category(database, db_category)
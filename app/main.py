from fastapi import FastAPI
from app.api import categories, books

from .db.db import SessionLocal
from .db.models import Category, Book
from sqlalchemy import select

# Описание ручек и приложения FastAPI
app = FastAPI(title="Octagon Book Store")

# Эндпоинт /health
@app.get("/health", tags=["system"])
def health_check():
    return {
        "status": "ok",
        "message": "Service is healthy and running"
    }

app.include_router(categories.router)
app.include_router(books.router)

# Вывод содержания таблиц
with SessionLocal() as session:
    categories = session.scalars(select(Category)).all()
    print("--- КАТЕГОРИИ ---")
    for cat in categories:
        print(f'ID: {cat.id} | Название: {cat.title}')

    books = session.scalars(select(Book)).all()
    print(f"\n--- КНИГИ ---")
    for book in books:
        print(f"ID: {book.id} | Название: {book.title}")

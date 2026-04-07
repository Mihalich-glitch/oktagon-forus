from fastapi import FastAPI
from app.api import categories, books

app = FastAPI(title="Octagon Book Store")

app.include_router(categories.router)
app.include_router(books.router)
from app.db.db import engine, Base, SessionLocal
from app.db.models import Category, Book # Импорт моделей обязателен!

def init_db():
    print("Создание таблиц в PostgreSQL...")
    # Удаляем и создаем заново для чистоты эксперимента (опционально)
    # Base.metadata.drop_all(bind=engine) 
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        # Проверяем, не пуста ли база, чтобы не дублировать данные
        if db.query(Category).first() is None:
            print("Наполнение базы тестовыми данными...")
            
            # 1. Создаем категории
            c1 = Category(title="Программирование")
            c2 = Category(title="Фантастика")
            db.add_all([c1, c2])
            db.flush() # Получаем ID категорий

            # 2. Создаем книги
            b1 = Book(title="Fluent Python", price=2500, category_id=c1.id)
            b2 = Book(title="Чистая Архитектура", price=1800, category_id=c1.id)
            b3 = Book(title="Марсианин", price=900, category_id=c2.id)
            b4 = Book(title="Автостопом по Галактике", price=750, category_id=c2.id)
            
            db.add_all([b1, b2, b3, b4])
            db.commit()
            print("Готово! Данные добавлены.")
        else:
            print("База уже содержит данные, пропускаю наполнение.")
            
    except Exception as e:
        db.rollback()
        print(f"Произошла ошибка: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    init_db()
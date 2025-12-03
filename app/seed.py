# app/seed.py
import json
from sqlalchemy import insert, select, delete
from app.db import async_session
from app.models import Product

async def load_products():
    async with async_session() as session:
        # 1. Удаляем старые товары
        await session.execute(delete(Product))
        await session.commit()

        print("Все старые товары удалены.")

        # 2. Загружаем JSON
        with open("app/static/products/products.json", "r", encoding="utf-8") as f:
            products = json.load(f)

        for p in products:
            stmt = insert(Product).values(
                title=p["title"],
                price=p["price"],
                description=p["description"],
                image=p["image"]
            )
            await session.execute(stmt)

        await session.commit()

        print(f"Добавлено товаров: {len(products)}")

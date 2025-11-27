# app/seed.py
import json
import asyncio
from sqlalchemy import insert, select
from app.db import async_session
from app.models import Product


async def load_products():
    async with async_session() as session:
        # Проверяем, есть ли товары
        result = await session.execute(select(Product))
        existing = result.scalars().all()

        if existing:
            print("Товары уже есть — пропуск.")
            return

        # читаем JSON
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
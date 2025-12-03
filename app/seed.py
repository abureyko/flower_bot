# app/seed.py
from sqlalchemy import insert, delete
from app.db import async_session
from app.models import Product
from app.seed_data import PRODUCTS

async def load_products():
    async with async_session() as session:
        # Удаляем все старые записи (чистый сид)
        await session.execute(delete(Product))
        await session.commit()

        # Вставляем заново
        for p in PRODUCTS:
            stmt = insert(Product).values(
                title=p["title"],
                price=p["price"],
                description=p.get("description"),
                image=p["image"]
            )
            await session.execute(stmt)

        await session.commit()

    print(f"Добавлено товаров: {len(PRODUCTS)}")
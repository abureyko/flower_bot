# app/main.py
import os
import asyncio
import logging
from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from aiogram.types import Update
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import FileResponse

from .db import Base, engine, get_db
from .models import Product, CartItem
from .bot import bot, dp

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# ---- STATIC FILES ----
app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/")
async def root():
    return FileResponse(os.path.join("app", "static", "index.html"))

# ---- DB MIGRATION + WEBHOOK ----
@app.on_event("startup")
async def on_startup():
    # create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    public = os.getenv("PUBLIC_URL")
    if public:
        webhook_url = f"{public}/tg_webhook"
        await bot.set_webhook(webhook_url)
        logger.info("Webhook set: %s", webhook_url)
    else:
        logger.warning("PUBLIC_URL is not set. Webhook will not work.")


@app.on_event("shutdown")
async def on_shutdown():
    await bot.session.close()


# ---- TELEGRAM WEBHOOK ----
@app.post("/tg_webhook")
async def tg_webhook(request: Request):
    try:
        data = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON")

    update = Update(**data)

    # ❗❗ ВАЖНО — правильный метод aiogram 3.x
    asyncio.create_task(dp.feed_webhook_update(bot, update))

    return {"ok": True}


# ---- API ----
@app.get("/api/products")
async def get_products(db: AsyncSession = Depends(get_db)):
    q = await db.execute(select(Product))
    items = q.scalars().all()
    return [
        {
            "id": p.id,
            "title": p.title,
            "price": p.price,
            "description": p.description,
            "image": p.image
        }
        for p in items
    ]


@app.post("/api/cart/add")
async def add_to_cart(payload: dict, db: AsyncSession = Depends(get_db)):
    user_id = str(payload.get("user_id"))
    product_id = int(payload.get("product_id"))
    qty = int(payload.get("qty", 1))

    item = CartItem(user_id=user_id, product_id=product_id, qty=qty)
    db.add(item)
    await db.commit()

    return {"status": "ok"}
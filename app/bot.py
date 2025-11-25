# app/bot.py
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
from aiogram.filters import Command

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN is required")

WEBAPP_URL = os.getenv("WEBAPP_URL", "https://example.com")

bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher()


# ✔️ Правильный фильтр для двух команд
@dp.message(Command(commands=["start", "help"]))
async def cmd_start(msg: types.Message):
    kb = ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [KeyboardButton(text="О компании")],
            [KeyboardButton(text="Помощь")],
            [KeyboardButton(text="Связаться с менеджером")],
            [KeyboardButton(text="Открыть веб-приложение", web_app=WebAppInfo(url=WEBAPP_URL))]
        ]
    )
    await msg.answer("Добро пожаловать!", reply_markup=kb)


@dp.message()
async def fallback(msg: types.Message):
    text = msg.text.lower() if msg.text else ""

    if "о компании" in text:
        await msg.answer("Мы тестовый магазин. Скоро будет больше функционала.")
    elif "помощ" in text:
        await msg.answer("Напиши /start чтобы начать заново.")
    elif "менеджер" in text:
        await msg.answer("Связь с менеджером: @SSIRRISS")
    else:
        await msg.answer("Команду не понял. Нажми /start.")
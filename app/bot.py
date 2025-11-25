# app/bot.py
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN is required")

WEBAPP_URL = os.getenv("WEBAPP_URL", "https://example.com")

bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher()

@dp.message(commands=["start", "help"])
async def cmd_start(msg: types.Message):
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(
        KeyboardButton(
            text="Открыть приложение",
            web_app=WebAppInfo(url=WEBAPP_URL)
        )
    )
    kb.add(KeyboardButton(text="О компании"))
    kb.add(KeyboardButton(text="Помощь"))
    kb.add(KeyboardButton(text="Связаться с менеджером"))

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
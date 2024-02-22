import asyncio
import logging
import os
import sys
from contextlib import suppress

from aiogram import Bot, Dispatcher, F
from aiogram.enums import ParseMode
from aiogram.types import Message, CallbackQuery
from dotenv_vault import load_dotenv
from aiogram.exceptions import TelegramBadRequest

import keyboards

load_dotenv()
TOKEN = os.getenv("token")
logging.basicConfig(level=logging.INFO)
dp = Dispatcher()


@dp.message(F.text == "/start")
async def start(message: Message):
    await message.answer(f"Привет 👋! Похоже вы не зарегистрированы. Введите класс в котором вы учитесь",
                         reply_markup=keyboards.paginator())


@dp.callback_query(keyboards.Pagination.filter(F.action.in_(["prev", "next"])))
async def pagination_handler(call: CallbackQuery, callback_data: keyboards.Pagination):
    page_num = int(callback_data.page)
    page = page_num - 1 if page_num > 0 else 0
    if callback_data.action == "next":
        page = page_num + 1 if page_num < (len("smth") - 1) else page_num
    with suppress(TelegramBadRequest):
        await call.message.edit_text(
            f"some text {page}",
            reply_markup=keyboards.paginator(page)
        )
    await call.answer()


async def main() -> None:
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())

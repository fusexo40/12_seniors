import asyncio
import logging
import os
import sys
from contextlib import suppress
import psycopg2


from aiogram import Bot, Dispatcher, F, Router
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.enums import ParseMode
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
from dotenv_vault import load_dotenv
from aiogram.filters import StateFilter, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage


import keyboards


try:
    conn = psycopg2.connect(dbname='users', user='postgres', password='root', host='localhost')
    print("Connection success")
except:
    print('Can`t establish connection to database')


load_dotenv()
TOKEN = "6906215709:AAEK45IdZPykFa2GYAtvFyN_5Wg2485b-Po"
print(TOKEN)
logging.basicConfig(level=logging.INFO)
bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher()
router = Router()
dp.include_router(router)

class UserStates(StatesGroup):
    NOTREGISTER = State()

@dp.message(CommandStart, StateFilter(None))
async def start(message: Message, state: FSMContext):
        cursor = conn.cursor()
        info = cursor.execute(f"SELECT id FROM userdb WHERE id={message.from_user.id}")
        print(info)
        cursor.close()
        await state.clear()
        if info is None:
            await state.set_state(UserStates.NOTREGISTER)
            current_state = await state.get_state()
            print(UserStates.NOTREGISTER)
            print(current_state)
        else:
            await message.answer("Первет", reply_markup=keyboards.main_kb )


@router.message(UserStates.NOTREGISTER)
async def not_registered(message: Message, state: FSMContext):
    print('fvgbhnj')
    await message.answer("Первет, Ты не зареган, чушпан. Введи свой класс обучения")
    form = message.text
    with conn.cursor as cursor:
        cursor.execute(f"""
                    INSERT INTO users (id, username, form, rating) VALUES ({message.from_user.id}, '{message.from_user.username}', {form}, 1000)
                    """)


@dp.callback_query(keyboards.Paginatorr.filter(F.action == "ask"))
async def add_question(message: Message):  
    pass


@dp.callback_query(keyboards.Paginatorr.filter(F.action == "profile"))
async def profile(message: Message):
    with conn.cursor as cursor:
        await message.answer(text=f"""Ник: {message.from_user.username}\nАктивных вопросов:
                                    {len(cursor.execute('SELECT question FROM questions WHERE author_id=?',
                                    (message.from_user.id, )).fetchall())}\nРейтинг: {1000}""",
                                    reply_markup=keyboards.profile_kb)


@dp.callback_query(keyboards.Paginatorr.filter(F.action == "back"))
async def mainmenu(message: Message):
    await message.answer("ИДИ НАЗУЙ", reply_markup=keyboards.back_kb)


@dp.callback_query(keyboards.Paginatorr.filter(F.action == "qlist"))
async def mainmenu(message: Message):
    await message.answer("Список ваших вопросов", reply_markup=keyboards.paginator_questions_list())


@dp.callback_query(keyboards.Paginatorr.filter(F.action == "link"))
async def tgk(message: Message):
    await message.answer("Ссылка на телеграм сообщество", reply_markup=keyboards.link_kb)


@dp.callback_query(keyboards.Pagination.filter(F.action.in_(["prev", "next", "page"])))
async def pagination_handler(call: CallbackQuery, callback_data: keyboards.Pagination):
    page_num = int(callback_data.page)
    if callback_data.action == "prev":
        page_num -= 1 if page_num > 0 else 0
    if callback_data.action == "next":
        page_num += 1 if page_num < (len("smth") - 1) else 0
    with suppress(TelegramBadRequest):
        await call.message.edit_text(
            f"some text {page_num}",
            reply_markup=keyboards.paginator(page_num)
        )
    await call.answer()


async def main() -> None:
    await dp.start_polling(bot)


async def clear(self) -> None:
    await self.set_state(None)
    await self.set_data({})


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())

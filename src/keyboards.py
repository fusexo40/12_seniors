from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData
from aiogram.filters import Command


items = [
        "1", "2", "3",
        "4", "5", "6",
        "7", "8", "9",
        "10", "11"
    ]


class Pagination(CallbackData, prefix="pag"):
    action: str
    page: int
    pages_count: int


class Paginatorr(CallbackData, prefix="pagi"):
    action: str


def paginator_questions_list(page: int = 0):
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="⬅", callback_data=Pagination(action="prev", page=page).pack()),
        InlineKeyboardButton(text=f"{page + 1}", callback_data=Pagination(action="page", page=page).pack()),
        InlineKeyboardButton(text="➡", callback_data=Pagination(action="next", page=page).pack()),
        width=3
    )
    return builder.as_markup()


def class_kb():
    builder = ReplyKeyboardBuilder()
    [builder.button(text=item) for item in items]
    builder.adjust(*[3] * 4)
    return builder.as_markup(resize_keyboard=True)


link_kb = InlineKeyboardMarkup(
    inline_keyboard=[
            [
            InlineKeyboardButton(text="Жмяк", url="tg://resolve?domain=dz_helper_chanel")
            ]
        ]
    )


back_kb = ReplyKeyboardMarkup(keyboard=[
            [
            KeyboardButton(text="Главное меню")
            ]
        ]
    )


profile_kb = ReplyKeyboardMarkup(keyboard=[
            [
            KeyboardButton(text="Мои вопросы", callback_data=Paginatorr(action="qlist")),
            KeyboardButton(text="Главное меню", callback_data=Paginatorr(action="back"))
            ]
        ]
    )


main_kb = ReplyKeyboardMarkup(keyboard=[
            [
            KeyboardButton(text="Задать вопрос", callback_data=Paginatorr(action="ask")),
            KeyboardButton(text="Профиль", callback_data=Paginatorr(action="profile")),
            KeyboardButton(text="Ссылка", callback_data=Paginatorr(action="link"))
            ]
        ]
    )

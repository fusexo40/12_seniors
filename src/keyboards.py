from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData


class Pagination(CallbackData, prefix="pag"):
    action: str
    page: int
    pages_count: int


def paginator(page: int = 0):
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="⬅", callback_data=Pagination(action="prev", page=page).pack()),
        InlineKeyboardButton(text=f"{page + 1}", callback_data=Pagination(action="page", page=page).pack()),
        InlineKeyboardButton(text="➡", callback_data=Pagination(action="next", page=page).pack()),
        width=3
    )
    return builder.as_markup()


def class_kb():
    items = [
        "1", "2", "3",
        "4", "5", "6",
        "7", "8", "9",
        "10", "11"
    ]
    builder = ReplyKeyboardBuilder()
    [builder.button(text=item) for item in items]
    builder.adjust(*[3] * 4)
    return builder.as_markup(resize_keyboard=True)


link_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Наше сообщество", url="tg://resolve?domain=dz_helper_chanel")
        ]
    ]
)



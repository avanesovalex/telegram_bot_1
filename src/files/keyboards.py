from aiogram.types import (InlineKeyboardMarkup, InlineKeyboardButton,
                           ReplyKeyboardMarkup, KeyboardButton)
from aiogram.utils.keyboard import InlineKeyboardBuilder


get_phone_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Отправить номер телефона📞',
                        request_contact=True)]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

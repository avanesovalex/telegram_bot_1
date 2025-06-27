from aiogram.types import (InlineKeyboardMarkup, InlineKeyboardButton,
                           ReplyKeyboardMarkup, KeyboardButton)
from aiogram.utils.keyboard import InlineKeyboardBuilder

from src.database.repositories.admin import get_all_users, get_one_user


get_phone_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Отправить номер телефона📞',
                        request_contact=True)]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

admin_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Добавить/Удалить сотрудников',
                              callback_data='users_page_0')]
    ]
)


async def get_users_kb(page=0, users_per_page=5) -> InlineKeyboardBuilder:
    users = await get_all_users()
    total_pages = max(1, (len(users) + users_per_page - 1) //
                      users_per_page)

    builder = InlineKeyboardBuilder()

    # Добавляем кнопки пользователей
    for user in users[page*users_per_page: (page+1)*users_per_page]:
        user_data = await get_one_user(user['user_id'])
        emoji = '✅' if user_data[2] else '👤'
        builder.button(
            text=f'{emoji}{user_data[1]}',
            callback_data=f"toggle_employee_{user_data[0]}_{page}"
        )

    builder.adjust(1)

    # Добавляем кнопки пагинации
    pagination_buttons = []

    prev_page = (page - 1) % total_pages
    pagination_buttons.append(InlineKeyboardButton(
        text="⬅️", callback_data=f"users_page_{prev_page}"))

    pagination_buttons.append(InlineKeyboardButton(
        text=f"{page+1}/{total_pages}", callback_data="current_page"))

    next_page = (page + 1) % total_pages
    pagination_buttons.append(InlineKeyboardButton(
        text="➡️", callback_data=f"users_page_{next_page}"))

    builder.row(*pagination_buttons)

    # Добавляем кнопку "В меню"
    builder.row(InlineKeyboardButton(text="Завершить",
                callback_data="back_to_admin_kb"))

    return builder

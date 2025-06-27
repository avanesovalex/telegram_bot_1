from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from src.files.filters import AdminFilter
from src.files.keyboards import admin_kb, get_users_kb
from src.database.repositories.user import update_employee_status


router = Router()


@router.message(Command('admin'), AdminFilter())
async def admin_menu(message: Message):
    await message.answer('Выберите действие', reply_markup=admin_kb)


@router.callback_query(F.data == 'back_to_admin_kb')
async def back_to_admin(callback: CallbackQuery):
    await callback.message.delete()  # type: ignore
    # type: ignore
    await callback.message.answer('Выберите действие', reply_markup=admin_kb)


@router.callback_query(F.data.startswith('users_page_'))
async def get_users_list(callback: CallbackQuery):
    page = int(callback.data.split('_')[-1])  # type: ignore
    builder = await get_users_kb(page=page)
    await callback.message.edit_text(  # type: ignore
        "Список пользователей:",
        reply_markup=builder.as_markup()
    )


@router.callback_query(F.data.startswith('toggle_employee'))
async def toggle_employee_status(callback: CallbackQuery):
    user_id = int(callback.data.split('_')[-2])  # type: ignore
    page = int(callback.data.split('_')[-1])  # type: ignore

    await update_employee_status(user_id)

    builder = await get_users_kb(page=page)
    await callback.message.edit_text(  # type: ignore
        "Список пользователей:",
        reply_markup=builder.as_markup()
    )

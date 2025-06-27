from aiogram.types import BotCommand, BotCommandScopeChat
from src.database.repositories.admin import get_all_admins


async def set_commands(bot):
    # Общие команды для всех пользователей
    user_commands = [
        BotCommand(command="start", description="Запуск бота"),
    ]

    # Команды только для админов
    admin_commands = user_commands + [
        BotCommand(command="admin", description="Админ-панель"),
    ]

    await bot.set_my_commands(user_commands)

    admins = await get_all_admins()
    for admin in admins:
        await bot.set_my_commands(admin_commands, scope=BotCommandScopeChat(chat_id=admin['user_id']))

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from aiogram import Bot

from src.database.repositories.admin import get_all_employees, get_pending_employees, get_all_admins
from src.database.repositories.request import sent_request_set_false
from src.files.keyboards import fill_request_kb


async def send_request_notification(bot: Bot):
    employees = await get_all_employees()
    await sent_request_set_false()

    if not employees:
        return

    for employee in employees:
        await bot.send_message(
            chat_id=employee['user_id'],
            text='Пожалуйста, заполните ежедневную заявку',
            reply_markup=fill_request_kb
        )


async def send_admin_notification(bot: Bot):
    pending = await get_pending_employees()

    if not pending:
        return

    admins = await get_all_admins()

    msg = '⚠Следующие сотрудники не заполнили заявку:\n'
    msg += '\n'.join(f'- {user['full_name']}' for user in pending)

    for admin in admins:
        await bot.send_message(
            chat_id=admin['user_id'],
            text=msg,
            parse_mode="Markdown"
        )


async def setup_scheduler(bot: Bot):
    scheduler = AsyncIOScheduler(timezone='Europe/Moscow')

    scheduler.add_job(
        send_request_notification,
        CronTrigger(day_of_week='mon-sat', hour=17, minute=0),
        kwargs={'bot': bot},
        name='employee_notification'
    )

    scheduler.add_job(
        send_admin_notification,
        CronTrigger(day_of_week='mon-sat', hour=17, minute=30),
        kwargs={'bot': bot},
        name='admin_notification'
    )

    scheduler.start()
    return scheduler

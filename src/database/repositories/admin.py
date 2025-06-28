from src.database.db import db


async def get_all_admins():
    admins = await db.fetch(
        '''SELECT user_id FROM users WHERE is_admin = TRUE'''
    )

    return [dict(admin) for admin in admins]


async def get_all_employees():
    employees = await db.fetch(
        '''SELECT user_id FROM users WHERE is_employee = TRUE'''
    )

    return [dict(employee) for employee in employees]


async def get_all_users():
    users = await db.fetch(
        '''SELECT user_id FROM users ORDER BY full_name'''
    )

    return [dict(user) for user in users]


async def get_one_user(user_id):
    user = await db.fetch(
        '''SELECT user_id, full_name, is_employee FROM users WHERE user_id = $1''', user_id
    )

    return [user[0]['user_id'],
            user[0]['full_name'],
            user[0]['is_employee']]


async def is_user_admin(user_id):
    is_admin = await db.fetchval(
        '''SELECT is_admin FROM users WHERE user_id = $1''', user_id
    )
    return is_admin


async def get_pending_employees():
    employees = await db.fetch(
        '''SELECT user_id, full_name FROM users
        WHERE is_employee = true AND sent_request = false'''
    )

    return [dict(employee) for employee in employees]

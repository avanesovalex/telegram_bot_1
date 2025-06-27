from src.database.db import db


async def get_all_admins():
    admins = await db.fetch(
        '''SELECT user_id FROM users WHERE is_admin = TRUE'''
    )

    return [dict(admin) for admin in admins]

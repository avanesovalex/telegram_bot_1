from src.database.db import db


async def sent_request_set_false():
    await db.execute(
        '''UPDATE users
        SET sent_request = false
        WHERE sent_request = true'''
    )


async def sent_request_set_true(user_id):
    await db.execute(
        '''UPDATE users
        SET sent_request = true
        WHERE user_id = $1''',
        user_id
    )

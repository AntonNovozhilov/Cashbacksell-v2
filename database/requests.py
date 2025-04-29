from database.models import async_session
from database.models import User, EventLog
from sqlalchemy import select


async def add_user(tg_id, username=None, first_name=None, last_name=None):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))
        if not user:
            session.add(User(
                tg_id=tg_id,
                username=username,
                first_name=first_name,
                last_name=last_name))
            await session.commit()


async def count_users():
    async with async_session() as session:
        return await session.scalars(select(User))
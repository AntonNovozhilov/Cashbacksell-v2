from database.models import async_session
from database.models import User, EventLog
from sqlalchemy import select
from datetime import datetime, timedelta, timezone

UTC_PLUS_4 = timezone(timedelta(hours=4))
now = datetime.now(UTC_PLUS_4)
start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
end_of_day = now.replace(hour=23, minute=59, second=59, microsecond=999999)
week_ago = now - timedelta(days=7)


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
    
async def count_users_today():
    async with async_session() as session:
        return await session.scalars(select(User).where(
            User.created_at >= start_of_day.astimezone(timezone.utc),
            User.created_at <= end_of_day.astimezone(timezone.utc)))
    
async def count_users_week():
    async with async_session() as session:
        return await session.scalars(select(User).where(
            User.created_at >= week_ago.astimezone(timezone.utc)))
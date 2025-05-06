from database.models import async_session, User, EventLog, ChatPrivatUser
from sqlalchemy import select, and_
from datetime import datetime, timedelta, timezone

UTC_PLUS_4 = timezone(timedelta(hours=4))
now = datetime.now(UTC_PLUS_4)
start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=1)
end_of_day = now.replace(hour=23, minute=59, second=59, microsecond=999999)
week_ago = now - timedelta(days=7)
month_ago = now - timedelta(days=30)


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
    
async def count_users_tg_id_list():
    async with async_session() as session:
        result = await session.scalars(select(User.tg_id))
        return result.all()
    
async def count_users_today():
    async with async_session() as session:
        return await session.scalars(select(User).where(
            User.created_at >= start_of_day.astimezone(timezone.utc),
            User.created_at <= end_of_day.astimezone(timezone.utc)))
    
async def count_users_week():
    async with async_session() as session:
        return await session.scalars(select(User).where(
            User.created_at >= week_ago.astimezone(timezone.utc)))
    
async def caht_add(tg_id, thread_id):
    async with async_session() as session:
        chat_user = await session.scalar(select(ChatPrivatUser).where(ChatPrivatUser.user_id==tg_id))
        if not chat_user:
            session.add(ChatPrivatUser(
                user_id=tg_id,
                thread_id=thread_id)
            )
            await session.commit()

async def chat_privat(tg_id):
    async with async_session() as session:
        result = await session.scalars(
            select(ChatPrivatUser.user_id).where(ChatPrivatUser.user_id == tg_id)
        )
        return result.all()
    
async def price_barter_add(tg_id):
    async with async_session() as session:
        event = EventLog(
            user_id=tg_id,
            event_type='price_barter',
            created_at=now
        )
        session.add(event)
        await session.commit()

async def count_price_barter():
    async with async_session() as session:
        return await session.scalars(select(EventLog).where(EventLog.event_type == 'price_barter'))


async def count_price_barter_today():
    async with async_session() as session:
        return await session.scalars(
            select(EventLog).where(
                and_(
                    EventLog.event_type == 'price_barter',
                    EventLog.created_at >= start_of_day.astimezone(timezone.utc),
                    EventLog.created_at <= end_of_day.astimezone(timezone.utc)
                )
            )
        )

    
async def count_price_barter_week():
    async with async_session() as session:
        return await session.scalars(select(EventLog).where(
            and_(EventLog.created_at >= week_ago.astimezone(timezone.utc), EventLog.event_type == 'price_barter')))
    
async def count_price_barter_month():
    async with async_session() as session:
        return await session.scalars(select(EventLog).where(
            and_(EventLog.created_at >= month_ago.astimezone(timezone.utc), EventLog.event_type == 'price_barter')))
    
async def price_cashback_add(tg_id):
    async with async_session() as session:
        event = EventLog(
            user_id=tg_id,
            event_type='price_cash',
            created_at=now
        )
        session.add(event)
        await session.commit()

async def count_price_cashback():
    async with async_session() as session:
        return await session.scalars(select(EventLog).where(EventLog.event_type == 'price_cash'))


async def count_price_cashback_today():
    async with async_session() as session:
        return await session.scalars(
            select(EventLog).where(
                and_(
                    EventLog.event_type == 'price_cash',
                    EventLog.created_at >= start_of_day.astimezone(timezone.utc),
                    EventLog.created_at <= end_of_day.astimezone(timezone.utc)
                )
            )
        )

    
async def count_price_cashback_week():
    async with async_session() as session:
        return await session.scalars(select(EventLog).where(
            and_(EventLog.created_at >= week_ago.astimezone(timezone.utc), EventLog.event_type == 'price_cash')))
    
async def count_price_cashback_month():
    async with async_session() as session:
        return await session.scalars(select(EventLog).where(
            and_(EventLog.created_at >= month_ago.astimezone(timezone.utc), EventLog.event_type == 'price_cash')))
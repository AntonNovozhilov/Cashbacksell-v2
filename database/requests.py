from datetime import datetime, timedelta, timezone

from sqlalchemy import select, and_

from database.models import async_session, User, EventLog, ChatPrivatUser

UTC_PLUS_4 = timezone(timedelta(hours=4))
now = datetime.now(UTC_PLUS_4)
start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=1)
end_of_day = now.replace(hour=23, minute=59, second=59, microsecond=999999)
week_ago = now - timedelta(days=7)
month_ago = now - timedelta(days=30)

async def add_user(tg_id, username=None, first_name=None, last_name=None):
    '''Добавление пользователя.'''
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
    '''Подсчет пользователей.'''
    async with async_session() as session:
        return await session.scalars(select(User))

async def count_users_tg_id_list():
    '''Вывод всех телеграм айди.'''
    async with async_session() as session:
        result = await session.scalars(select(User.tg_id))
        return result.all()

async def count_users_today():
    '''Сколько подписалось сегодня.'''
    async with async_session() as session:
        return await session.scalars(select(User).where(
            User.created_at >= start_of_day.astimezone(timezone.utc),
            User.created_at <= end_of_day.astimezone(timezone.utc)))

async def count_users_week():
    '''Сколько подписалось за неделю.'''
    async with async_session() as session:
        return await session.scalars(select(User).where(
            User.created_at >= week_ago.astimezone(timezone.utc)))

async def caht_add(tg_id, thread_id):
    '''Добавление чата в базу.'''
    async with async_session() as session:
        chat_user = await session.scalar(
            select(ChatPrivatUser).where(ChatPrivatUser.user_id==tg_id))
        if not chat_user:
            session.add(ChatPrivatUser(
                user_id=tg_id,
                thread_id=thread_id)
            )
            await session.commit()

async def chat_privat(tg_id):
    '''Список чатов.'''
    async with async_session() as session:
        result = await session.scalars(
            select(
                ChatPrivatUser.user_id).where(ChatPrivatUser.user_id == tg_id)
        )
        return result.all()

async def price_barter_add(tg_id):
    '''Добавление событий по запросу стоимости бартера.'''
    async with async_session() as session:
        event = EventLog(
            user_id=tg_id,
            event_type='price_barter',
            created_at=now
        )
        session.add(event)
        await session.commit()

async def count_price_barter():
    '''Подсчет кол-ва запроса стоимости бартера.'''
    async with async_session() as session:
        return await session.scalars(
            select(EventLog).where(EventLog.event_type == 'price_barter'))

async def count_price_barter_today():
    '''Подсчет кол-ва запроса стоимости бартера за сегодня.'''
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
    '''Подсчет кол-ва запроса стоимости бартера за неделю.'''
    async with async_session() as session:
        return await session.scalars(select(EventLog).where(
            and_(EventLog.created_at >= week_ago.astimezone(timezone.utc), EventLog.event_type == 'price_barter')))

async def count_price_barter_month():
    '''Подсчет кол-ва запроса стоимости бартера за месяц.'''
    async with async_session() as session:
        return await session.scalars(select(EventLog).where(
            and_(EventLog.created_at >= month_ago.astimezone(timezone.utc), EventLog.event_type == 'price_barter')))

async def price_cashback_add(tg_id):
    '''Добавление событий по запросу стоимости кешбека.'''
    async with async_session() as session:
        event = EventLog(
            user_id=tg_id,
            event_type='price_cash',
            created_at=now
        )
        session.add(event)
        await session.commit()

async def count_price_cashback():
    '''Подсчет кол-ва запроса стоимости бартера.'''
    async with async_session() as session:
        return await session.scalars(select(EventLog).where(EventLog.event_type == 'price_cash'))

async def count_price_cashback_today():
    '''Подсчет кол-ва запроса стоимости бартера за сегодня.'''
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
    '''Подсчет кол-ва запроса стоимости бартера за неделю.'''
    async with async_session() as session:
        return await session.scalars(
            select(EventLog).where(
            and_(EventLog.created_at >= week_ago.astimezone(timezone.utc),
                 EventLog.event_type == 'price_cash'))
                 )

async def count_price_cashback_month():
    '''Подсчет кол-ва запроса стоимости бартера за месяц.'''
    async with async_session() as session:
        return await session.scalars(
            select(EventLog).where(
            and_(EventLog.created_at >= month_ago.astimezone(timezone.utc),
                 EventLog.event_type == 'price_cash'))
                 )
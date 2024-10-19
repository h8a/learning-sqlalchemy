import asyncio
import os
import sys

from asyncio import current_task

from sqlalchemy import URL, select
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_scoped_session,
    async_sessionmaker,
    create_async_engine,
)

async_engine = create_async_engine(
    URL.create(
        drivername="postgresql+asyncpg",
        username="postgres",
        password=os.getenv("DB_PASS"),
        host=os.getenv("DB_HOST"),
        port=5432,
        database=os.getenv("DB_NAME"),
    )
)

async_session = async_scoped_session(
    async_sessionmaker(async_engine, expire_on_commit=False), scopefunc=current_task
)


async def db_psql_session() -> AsyncSession:
    session = async_session()
    return session


async def check_connection():
    session = await db_psql_session()
    await session.begin()
    try:
        result = await session.execute(select(1))
        print(f"SELECT 1: {result.scalar()}")
        await session.commit()
    except Exception as e:
        print(f"Error to try check connection: {e}")
        await session.rollback()
    finally:
        await session.close()


async def close_connection():
    try:
        await async_engine.dispose()
    except Exception as e:
        print(f"Error trying to close connection: {e}")
        sys.exit(-1)


async def main():
    await check_connection()
    await close_connection()


if __name__ == "__main__":
    asyncio.run(main())

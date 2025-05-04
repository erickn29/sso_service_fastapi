from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlalchemy.orm import DeclarativeBase


async def drop_and_create_tables(engine: AsyncEngine, base: type[DeclarativeBase]):
    async with engine.begin() as conn:
        await conn.run_sync(base.metadata.drop_all)
        await conn.run_sync(base.metadata.create_all)


async def create_engine(
    db_url: str, base: type[DeclarativeBase], refresh: bool = True
) -> AsyncEngine:
    engine = create_async_engine(
        db_url,
        echo=False,
        poolclass=NullPool,
    )
    if refresh:
        await drop_and_create_tables(engine, base)
    return engine


async def dispose_engine(engine: AsyncEngine):
    await engine.dispose()

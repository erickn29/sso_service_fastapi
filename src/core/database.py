from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from core.config import config as cfg


class DatabaseHelper:

    def __init__(
        self,
        url: str,
        echo: bool = False,
        echo_pool: bool = False,
        pool_size: int = 10,
        max_overflow: int = 20,
        pool_recycle: int = 600,
        pool_pre_ping: bool = True,
    ):
        self.engine = create_async_engine(
            url=url,
            echo=echo,
            echo_pool=echo_pool,
            pool_size=pool_size,
            max_overflow=max_overflow,
            pool_recycle=pool_recycle,
            pool_pre_ping=pool_pre_ping,
        )
        self.async_session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )

    @asynccontextmanager
    async def get_session(self):
        session = None
        try:
            session: AsyncSession = self.async_session_factory()
            yield session
            await session.commit()
        except Exception:  # noqa
            if session:
                await session.rollback()
        finally:
            if session:
                await session.close()


db_conn = DatabaseHelper(
    url=cfg.db.url(),
    echo=cfg.db.echo,
    echo_pool=cfg.db.echo_pool,
    pool_size=cfg.db.pool_size,
    max_overflow=cfg.db.max_overflow,
    pool_recycle=cfg.db.pool_recycle,
    pool_pre_ping=cfg.db.pool_pre_ping,
)

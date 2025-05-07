from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker


async def get_session(engine: AsyncEngine) -> AsyncSession:
    async_session_maker = async_sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False, autoflush=False
    )
    session: AsyncSession = async_session_maker()
    return session

from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.settings import conf


engine: AsyncEngine = create_async_engine(
    conf.pg_connection_string,
    pool_size=conf.PG_POOL_SIZE,
    future=True,
)
async_session: async_sessionmaker = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
    class_=AsyncSession,
)

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from consumer.database.base import ENGINE


async def make_session():  # noqa: ANN201
    async with sessionmaker(ENGINE, class_=AsyncSession)() as session:
        yield session

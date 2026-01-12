from sqlalchemy.ext.asyncio import create_async_engine

from consumer.settings import settings


ENGINE = create_async_engine(settings.db.url)

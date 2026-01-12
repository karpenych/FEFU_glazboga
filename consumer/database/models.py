from sqlalchemy import TEXT, TIMESTAMP, Column, Float, Integer
from sqlalchemy.orm import DeclarativeBase

from consumer.database.base import ENGINE
from consumer.logger import LOGGER


class Base(DeclarativeBase):
    pass


class DeviceModel(Base):
    __tablename__ = "devices"

    id = Column(TEXT, primary_key=True)
    location = Column(TEXT)
    type = Column(TEXT)
    unit = Column(TEXT)


class IoTEventModel(Base):
    __tablename__ = "iot_events"

    id = Column(Integer, primary_key=True, autoincrement=True)
    device_id = Column(TEXT)
    value = Column(Float)
    timestamp = Column(TIMESTAMP)


async def init_db() -> None:
    LOGGER.info("Creating tables...")
    async with ENGINE.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    LOGGER.info("Tables created!")

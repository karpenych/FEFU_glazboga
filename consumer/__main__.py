import asyncio
import logging

import orjson
from faststream import FastStream

import consumer.database.models as m
from consumer.entities import IoTEvent
from consumer.logger import LOGGER
from consumer.nats.broker import BROKER
from consumer.service.event_processor_service import IoTEventProcessor
from consumer.settings import settings


APP = FastStream(BROKER)

EVENT_PROCESSOR = IoTEventProcessor()


@BROKER.subscriber(settings.mq.subject)
async def process_event(msg: str) -> None:
    try:
        LOGGER.debug(f"raw msg: {msg}")
        event = IoTEvent(**orjson.loads(msg))
        await EVENT_PROCESSOR.process_event(event)
    except Exception as e:  # noqa: BLE001
        LOGGER.error(f"ERROR while processing msg: {e}")


async def main() -> None:
    LOGGER.info("\n##### CONSUMER started #####\n")
    LOGGER.info("<<< PARAMETERS >>>")
    LOGGER.info("NATS:")
    LOGGER.info(f" - server: {settings.mq.server}")
    LOGGER.info(f" - subject: {settings.mq.subject}")
    LOGGER.info("POSTGRES:")
    LOGGER.info(f" - url: {settings.db.url}")

    await m.init_db()
    await APP.run(log_level=logging.WARNING)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        LOGGER.info("### CONSUMER stopped by user ###")
    except Exception as ex:  # noqa: BLE001
        LOGGER.error(f"Error is occured: {ex}")
    finally:
        LOGGER.info("<<<<< CONSUMER stopped")

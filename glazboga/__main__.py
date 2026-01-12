import asyncio
import random
from typing import TYPE_CHECKING

from glazboga.logger import LOGGER
from glazboga.nats.broker import BROKER
from glazboga.nats.publishers import publish_event
from glazboga.service import IoTDataGenerator
from glazboga.settings import settings


if TYPE_CHECKING:
    from glazboga.entities import IoTEvent


async def _init_send_events_task(event_generator_srv: IoTDataGenerator) -> None:
    async with BROKER as broker:
        while True:
            event: IoTEvent = event_generator_srv.generate_event()
            LOGGER.debug(event.model_dump_json())

            await publish_event(broker, event)
            await asyncio.sleep(random.uniform(settings.min_task_sleep_time, settings.max_task_sleep_time))


async def main() -> None:
    LOGGER.info("\n##### GLAZBOGA started #####\n")

    LOGGER.info("<<< PARAMETERS >>>")
    LOGGER.info("NATS:")
    LOGGER.info(f" - server: {settings.mq.server}")
    LOGGER.info(f" - subject: {settings.mq.subject}")
    LOGGER.info("GLAZBOGA:")
    LOGGER.info(f" - locations_num: {settings.locations_num}")
    LOGGER.info(f" - tasks_num: {settings.tasks_num}")
    LOGGER.info(f" - min_task_sleep_time: {settings.min_task_sleep_time}")
    LOGGER.info(f" - max_task_sleep_time: {settings.max_task_sleep_time}")
    LOGGER.info("")

    event_generator_srv = IoTDataGenerator(locations_num=settings.locations_num)
    LOGGER.debug("\n".join(event_generator_srv.locations[:5]) + "\n...\n")

    tasks = [asyncio.create_task(_init_send_events_task(event_generator_srv)) for _ in range(settings.tasks_num)]

    await asyncio.gather(*tasks)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        LOGGER.info("### GLAZBOGA stopped by user ###")
    except Exception as ex:  # noqa: BLE001
        LOGGER.error(f"Error is occured: {ex}")
    finally:
        LOGGER.info("<<<<< GLAZBOGA stopped")

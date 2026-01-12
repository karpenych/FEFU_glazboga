from faststream.nats import NatsBroker

from glazboga.entities import IoTEvent
from glazboga.logger import LOGGER
from glazboga.settings import settings


async def publish_event(broker: NatsBroker, event: IoTEvent) -> None:
    try:
        await broker.publish(event.model_dump_json(), subject=settings.mq.subject)
    except Exception as exc:  # noqa: BLE001
        LOGGER.exception(f"ERROR while publis msg: {exc}")

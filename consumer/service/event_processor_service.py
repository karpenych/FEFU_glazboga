import datetime as dt
from dataclasses import dataclass

import consumer.database.models as m
from consumer.database.session import make_session
from consumer.entities import IoTEvent


@dataclass(kw_only=True, slots=True)
class IoTEventProcessor:
    async def process_event(self, event: IoTEvent) -> None:
        async for session in make_session():
            device_model = m.DeviceModel(
                id=event.device_id,
                location=event.location,
                type=event.device_type,
                unit=event.unit,
            )

            event_model = m.IoTEventModel(
                device_id=event.device_id,
                value=event.value,
                timestamp=dt.datetime.fromisoformat(event.timestamp),
            )

            await session.merge(device_model)
            session.add(event_model)

            await session.commit()

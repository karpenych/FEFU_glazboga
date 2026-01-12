import random
import uuid
from dataclasses import dataclass, field
from datetime import datetime

from faker import Faker

from glazboga.entities import Device, DeviceTypeParams, IoTEvent
from glazboga.enums import DeviceType, Unit


@dataclass(kw_only=True, slots=True)
class IoTDataGenerator:
    locations_num: int
    fake: Faker = field(init=False)
    sensor_conf: dict[DeviceType, DeviceTypeParams] = field(init=False)
    min_devices: int = field(init=False)
    max_devices: int = field(init=False)
    locations: list[str] = field(init=False)
    devices: list[Device] = field(init=False)

    def __post_init__(self) -> None:
        self.fake = Faker("ru_RU")
        self.sensor_conf = {
            DeviceType.TEMPERATURE: DeviceTypeParams(min=-20.0, max=50.0, unit=Unit.TEMPERATURE, unit_type="float"),
            DeviceType.HUMIDITY: DeviceTypeParams(min=0.0, max=100.0, unit=Unit.HUMIDITY, unit_type="float"),
            DeviceType.PRESSURE: DeviceTypeParams(min=950.0, max=1050.0, unit=Unit.PRESSURE, unit_type="float"),
            DeviceType.VIBRATION: DeviceTypeParams(min=0.0, max=10.0, unit=Unit.VIBRATION, unit_type="float"),
            DeviceType.CO2: DeviceTypeParams(min=300.0, max=2000.0, unit=Unit.CO2, unit_type="int"),
            DeviceType.LIGHT: DeviceTypeParams(min=0.0, max=10000.0, unit=Unit.LIGHT, unit_type="int"),
        }
        self.min_devices = 1
        self.max_devices = len(self.sensor_conf)
        self.locations = self._init_locations(self.locations_num)
        self.devices = self._init_devices(self.locations)

    def _init_locations(self, locations_num: int) -> list[str]:
        return [self.fake.address() for _ in range(locations_num)]

    def _init_devices(self, locations: list[str]) -> list[Device]:
        devices = []
        for one_location in locations:
            for device_type, device_params in self.sensor_conf.items():
                devices.append(
                    Device(
                        id=uuid.uuid4(),
                        type=device_type,
                        params=device_params,
                        location=one_location,
                    )
                )
        return devices

    def generate_value(self, device: Device) -> float:
        value = random.uniform(device.params.min, device.params.max)
        noise = random.uniform(-0.05, 0.05) * (device.params.max - device.params.min)
        value += noise

        anomaly_perc = 0.02
        anomaly_type_treshold = 0.5
        if random.random() < anomaly_perc:
            value = value * (0.1 if random.random() < anomaly_type_treshold else 1.8)

        return round(value, 2) if device.params.unit_type == "float" else float(int(value))

    def generate_event(self) -> IoTEvent:
        """Генерируем один объект IoTEvent (Pydantic-модель)."""
        device = random.choice(self.devices)
        return IoTEvent(
            device_id=str(device.id),
            device_type=device.type,
            location=device.location,
            value=self.generate_value(device),
            unit=device.params.unit,
            timestamp=datetime.now().isoformat(),  # noqa: DTZ005
        )

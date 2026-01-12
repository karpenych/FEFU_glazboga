from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from glazboga.enums import DeviceType, Unit


class DeviceTypeParams(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    min: float = Field(..., description="Минимальное значение")
    max: float = Field(..., description="Максимвльное значение")
    unit: Unit = Field(..., description="Мера")
    unit_type: str = Field(..., description="Тип меры (int | float)")


class Device(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    id: UUID = Field(..., description="Уникальный ID устройства")
    type: DeviceType = Field(..., description="Тип датчика")
    params: DeviceTypeParams = Field(..., description="Параметры датчика")
    location: str = Field(..., description="Местоположение устройства")


class IoTEvent(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    device_id: str = Field(..., description="Уникальный ID устройства")
    device_type: DeviceType = Field(..., description="Тип датчика")
    location: str = Field(..., description="Местоположение устройства")
    value: float = Field(..., description="Значение с датчика")
    unit: str = Field(..., description="Единица измерения")
    timestamp: str = Field(..., description="Время события (UTC)")

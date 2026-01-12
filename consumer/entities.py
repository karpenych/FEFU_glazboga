from pydantic import BaseModel


class IoTEvent(BaseModel):
    device_id: str
    device_type: str
    location: str
    value: float
    unit: str
    timestamp: str

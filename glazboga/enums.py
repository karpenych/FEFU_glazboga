from enum import StrEnum


class DeviceType(StrEnum):
    TEMPERATURE = "TEMPERATURE"
    HUMIDITY = "HUMIDITY"
    PRESSURE = "PRESSURE"
    VIBRATION = "VIBRATION"
    CO2 = "CO2"
    LIGHT = "LIGHT"


class Unit(StrEnum):
    TEMPERATURE = "C"
    HUMIDITY = "%"
    PRESSURE = "hPa"
    VIBRATION = "mm/s2"
    CO2 = "ppm"
    LIGHT = "lux"

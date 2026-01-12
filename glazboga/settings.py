import typing

from pydantic_settings import BaseSettings, SettingsConfigDict


class NatsSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="NATS_")

    server: str = "localhost:4222"
    subject: str = "glazboga.events"


class Settings(BaseSettings):
    locations_num: int = 1000
    tasks_num: int = 5

    min_task_sleep_time: float = 0.1
    max_task_sleep_time: float = 10.0

    log_lvl: str = "debug"

    mq: NatsSettings = NatsSettings()


settings: typing.Final = Settings()

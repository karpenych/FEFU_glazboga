from faststream.nats import NatsBroker

from glazboga.settings import settings


def create_nats_broker() -> NatsBroker:
    return NatsBroker(f"nats://{settings.mq.server}")


BROKER: NatsBroker = create_nats_broker()

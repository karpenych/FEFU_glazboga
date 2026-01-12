import logging
import sys

from consumer.settings import settings


LOGGER = logging.getLogger("CONSUMER")
LOGGER.setLevel(logging.DEBUG if settings.log_lvl == "debug" else logging.INFO)
LOGGER.addHandler(logging.StreamHandler(sys.stdout))

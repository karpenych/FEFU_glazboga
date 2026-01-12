import logging
import sys

from glazboga.settings import settings


LOGGER = logging.getLogger("GLAZBOGA")
LOGGER.setLevel(logging.DEBUG if settings.log_lvl == "debug" else logging.INFO)
LOGGER.addHandler(logging.StreamHandler(sys.stdout))

from logging import getLogger, FileHandler, DEBUG  # , StreamHandler

logger = getLogger(__name__)
logger.setLevel(DEBUG)

# ch = StreamHandler()
# ch.setLevel(INFO)

fh = FileHandler('agora.log')
fh.setLevel(DEBUG)

# logger.addHandler(ch)
logger.addHandler(fh)

__all__ = ('logger')

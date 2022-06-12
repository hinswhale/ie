import logging

logger = logging.getLogger(__name__)
logger.setLevel(level=logging.ERROR)
handler = logging.FileHandler('log/logfile.log')
logger.addHandler(handler)

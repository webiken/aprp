import logging
from logging.handlers import RotatingFileHandler
DEBUG = True

# for development we use port 8000
PORT = 80 if not DEBUG else 8000

# logging level of DEBUG in development
LOG_LEVEL = logging.INFO if not DEBUG else logging.DEBUG

#logging format
FORMAT = '%(asctime)-15s %(message)s'
formatter = logging.Formatter(FORMAT)
handler = RotatingFileHandler('./aprp.log', maxBytes=10000000, backupCount=5, encoding='utf-8')
handler.setFormatter(formatter)

# impor this logger in other parts of app
logger = logging.getLogger("Rotating Log")
logger.setLevel(LOG_LEVEL)
logger.addHandler(handler)

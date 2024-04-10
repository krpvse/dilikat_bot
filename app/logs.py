import logging
import logging.handlers


def init_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    f = '%(asctime)s // %(name)s:%(lineno)s // %(levelname)s // %(message)s'

    sh = logging.StreamHandler()
    sh.setFormatter(logging.Formatter(f))

    fh = logging.handlers.RotatingFileHandler(filename='logs/logs.log', maxBytes=10**6, backupCount=5)
    fh.setFormatter(logging.Formatter(f))
    fh.setLevel(logging.INFO)

    logger.addHandler(sh)
    logger.addHandler(fh)

    logger.debug('Logger was initialized')


bot_logger = logging.getLogger('bot')
notification_logger = logging.getLogger('bot.notifications')
db_logger = logging.getLogger('bot.database')

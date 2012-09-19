#!usr/bin/env python

import logging
from logging.handlers import RotatingFileHandler
from os import path
from os import makedirs


# create logger with 'classes'
logger = logging.getLogger('desk')
logger.setLevel(logging.DEBUG)

# create file handler which logs even debug messages
log_path = 'logs/desk.log'
log_dir, log_file = path.split(log_path)
if not path.exists(log_dir):
    makedirs(log_dir)
fh = RotatingFileHandler(log_path, maxBytes=20000, backupCount=5)
fh.setLevel(logging.DEBUG)

# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)

# create formatter and add it to the handlers
formatter = logging.Formatter(
        '%(levelname)-8s %(asctime)-15s %(name)-20s %(message)s'
        )
fh.setFormatter(formatter)
ch.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)

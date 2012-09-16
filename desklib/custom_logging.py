#!usr/bin/env python

import logging
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
fh = logging.FileHandler(log_path)
fh.setLevel(logging.DEBUG)

# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)

# create formatter and add it to the handlers
formatter = logging.Formatter(
        '%(levelname)s:%(asctime)s: %(name)s: %(message)s\n'
        )
fh.setFormatter(formatter)
ch.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)

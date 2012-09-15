#!usr/bin/env python

import logging

logging.basicConfig(
        filename='../logs/example.log',
        format='%(module)s : %(levelname)s : %(message)s',
        level=logging.DEBUG
        )

logging.debug('This message should go to the logfile.')
logging.info('So should this.')
logging.error('And this too.')

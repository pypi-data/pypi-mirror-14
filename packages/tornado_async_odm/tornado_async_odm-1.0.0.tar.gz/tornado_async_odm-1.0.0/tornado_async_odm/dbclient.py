import logging

import motor

logger = logging.getLogger(__name__)

# database connection
db_connection = None

# x509 authentication parameters
ssl = False
x509_username = None

def init(*args, **kwargs):
    logger.info('initializing database connection')
    global db_connection, ssl, x509_username
    ssl = kwargs['ssl']
    print('ssl: ' + str(ssl))

    try:
        x509_username = kwargs['x509_username']
        del kwargs['x509_username']
    except KeyError:
        pass

    db_connection = motor.MotorClient(*args, **kwargs)
    if db_connection:
        return True
    return False

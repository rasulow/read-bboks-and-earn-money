bind = "0.0.0.0:5050"
workers = 4

import logging
from logging.handlers import RotatingFileHandler

loglevel = 'info'
accesslog = '/home/administrator/read-books-and-earn-money/access.log'
errorlog = '/home/administrator/read-books-and-earn-money/error.log'

def setup_logging():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    access_handler = RotatingFileHandler(accesslog, maxBytes=10000000, backupCount=5)
    access_handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
    logging.getLogger('gunicorn.access').addHandler(access_handler)
    
    error_handler = RotatingFileHandler(errorlog, maxBytes=10000000, backupCount=5)
    error_handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
    logging.getLogger('gunicorn.error').addHandler(error_handler)

setup_logging()
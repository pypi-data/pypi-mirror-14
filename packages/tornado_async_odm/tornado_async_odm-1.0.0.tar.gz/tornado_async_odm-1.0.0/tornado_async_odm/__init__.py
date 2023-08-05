import logging

import re

import sys

__version__ = '1.0.0'

# Quick & Dirty solution for logging
'''
root = logging.getLogger()
root.setLevel(logging.INFO)
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
root.addHandler(ch)
'''

# initialize
logger = logging.getLogger(__name__)
logger.info('initializing tornado_async_odm ver. ' + __version__)

# Define database operation types
DB_INSERT = 'insert'
DB_UPDATE = 'update'
DB_REMOVE = 'remove'

# Define field types
TYPE_NONE = 'type_none'
TYPE_INT = 'type_int'
TYPE_BOOL = 'type_bool'
TYPE_DATE = 'type_date'
TYPE_STR = 'type_string'
TYPE_LOWER = 'type_string_lower'
TYPE_STR_A0 = 'type_string_a0'
TYPE_STR_LETTERS = 'type_string_letters'
TYPE_STR_ASPACE = 'type_string_aspace'
TYPE_EMAIL = 'type_email'
TYPE_PHONE = 'type_phone'
TYPE_PASSWORD = 'type_password'

# Regular expressions for field data validation
regex_aspace    = re.compile(r'^[a-zA-Z\s]*$')
regex_letters   = re.compile(r'^[a-zA-Z]+$')
regex_a0        = re.compile(r'^[\w]+$')
regex_email     = re.compile(r'[^@]+@[^@]+\.[^@]+')
# valid formats:
# 123-456-7890
# (123) 456-7890
# 123 456 7890
# 123.456.7890
# +91 (123) 456-7890
regex_phone     = re.compile(r'^(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]\d{3}[\s.-]\d{4}$')
# secure password
regex_password  = re.compile(r'(?=.*?[a-z])(?=.*?[A-Z])(?=.*?[^a-zA-Z]).{8,}')

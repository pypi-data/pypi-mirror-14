__author__ = 'Daniel Sanchez Prolongo'
__version__ = '1.0.5'

API_VERSION = 'v0.1'
API_URL = 'https://analytics.plytix.com/api/retailers/{version}'.format(version=API_VERSION)


def enum(**enums):
    return type('Enum', (), enums)

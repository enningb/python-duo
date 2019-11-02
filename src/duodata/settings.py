import os
import configparser
import logging

config = configparser.ConfigParser()
config.optionxform = str  # So capitals stay capitals

# File containing variables:
DUODATA_CONFIG = os.path.join(os.path.expanduser('~'), '.duodata.cfg')


if os.path.exists(DUODATA_CONFIG):
    logging.info('Reading %s...' % DUODATA_CONFIG)
    config.read(DUODATA_CONFIG)
    # Directory waar data wordt opgeslagen
    data_dir = config.get('algemeen', 'data_dir')

    # Google API key
    google_api_key = config.get('algemeen', 'google_api_key')

else:
    logging.error('Missing config-file: %s' % DUODATA_CONFIG)
    data_dir = os.path.join(os.path.expanduser('~'), 'duodata')

    # Google API key
    google_api_key = 'THIS IS NOT A KEY'

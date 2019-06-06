import os
import configparser
import logging
import future

config=configparser.ConfigParser()
config.optionxform=str # So capitals stay capitals

# File containing variables:
DUO_CONFIG = os.path.join(os.path.expanduser('~'), '.duo_data.cfg')


if os.path.exists(DUO_CONFIG):
    logging.info('Reading %s...' % DUO_CONFIG)
    config.read(DUO_CONFIG)
else:
    logging.error('Missing config-file: %s' % DUO_CONFIG)

# Directory waar data wordt opgeslagen
duo_data_dir=config.get('algemeen','duo_data_dir')

# Google API key
google_api_key=config.get('algemeen','google_api_key')
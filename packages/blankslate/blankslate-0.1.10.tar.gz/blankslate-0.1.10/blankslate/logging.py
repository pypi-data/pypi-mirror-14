from __future__ import absolute_import
import logging, os

if os.getenv('DEBUG'):
    logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('blankslate')

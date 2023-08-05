import logging
import sys

# init logger
logger = logging.getLogger(__package__)


def abort(errstr, errcode=1):
    logger.error(errstr)
    sys.exit(errcode)


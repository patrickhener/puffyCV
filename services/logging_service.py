import logging
import sys

from puffyCV.args import args


def initialize_logging():
    if args.DEBUG:
        logging_format = '%(levelname).1s %(asctime)-15s '
        logging_format += '%(filename)s:%(lineno)d %(message)s'
    else:
        logging_format = '%(levelname).1s %(asctime)-15s %(message)s'

    logging.basicConfig(
        stream=sys.stdout,
        level=logging.DEBUG if args.DEBUG else logging.INFO,
        format=logging_format,
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    log = logging.getLogger(__name__)

    return log

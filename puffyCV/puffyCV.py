#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import signal
import sys

import puffyCV.calibration
import puffyCV.recognition
from puffyCV.args import args
from puffyCV.logging import log

FORMAT = '%(levelname).1s %(asctime)-15s %(message)s'

logging.basicConfig(
    stream=sys.stdout,
    level=logging.DEBUG if args.DEBUG else logging.INFO,
    format=FORMAT,
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger(__name__)


def signal_handler(sig, frame):
    log.info("CTRL-C caught, exiting...")
    print("PRINT:CTRL-C caught, exiting...")


def main():
    signal.signal(signal.SIGINT, signal_handler)
    mode = args.MODE
    if args.MODE == "run":
        print("puffyCV recognition started")
        puffyCV.recognition.start_recognition()
    elif args.MODE == "cal":
        print("puffyCV calibration started")
        puffyCV.calibration.start_calibration()
    else:
        print("Invalid mode selected. Please refer to README.")

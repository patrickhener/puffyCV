#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import signal
import sys
import cv2

from puffyCV.args import args

from services.logging_service import initialize_logging
from services.calib_service import calibrate
from services.draw_service import Board

log = initialize_logging()


def signal_handler(sig, frame):
    log.info("CTRL-C caught, exiting...")
    sys.exit()


def main():
    signal.signal(signal.SIGINT, signal_handler)
    if args.MODE == "run":
        log.info("puffyCV recognition started")
    elif args.MODE == "cal":
        if len(args.DEVICE_IDS) > 1:
            log.error("Please provide one camera at a time to calibrate.")
            sys.exit()
        else:
            device_id = int(args.DEVICE_IDS[0])
        calibrate(device_id)
    elif args.MODE == "mytest":
        pass
    elif args.MODE == "mytest2":
        draw = Board(900)
        while True:
            cv2.imshow("test", draw.projection_prepare())
            c = cv2.waitKey(1)
            if 'q' == chr(c & 255):
                break

    else:
        log.error("Invalid mode selected. Please refer to README.")

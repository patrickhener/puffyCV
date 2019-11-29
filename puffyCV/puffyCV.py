#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import signal
import sys
import cv2

from puffyCV.args import args
from puffyCV.logging import log
from puffyCV.gameloop import GameLoop
from config.config_repo import create_config
from imageprocessing.capturingdevice import initialize_real_devices, configure_devices
from imageprocessing.draw import Draw
from positioning.dartboard import Board

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
    sys.exit()


def main():
    signal.signal(signal.SIGINT, signal_handler)
    if args.MODE == "run":
        log.info("puffyCV recognition started")
        devices = initialize_real_devices()
        create_config()
        game_loop = GameLoop(devices)
        game_loop.run()
    elif args.MODE == "cal":
        log.info("puffyCV calibration started")
        create_config()
        devices = initialize_real_devices()
        configure_devices(devices)
    elif args.MODE == "mytest":
        board = Board()
        board.print()
    elif args.MODE == "mytest2":
        draw = Draw(900)
        img = draw.projection_prepare()
        while True:
            cv2.imshow("test", img)
            c = cv2.waitKey(1)
            if 'q' == chr(c & 255):
                break

    else:
        log.error("Invalid mode selected. Please refer to README.")

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
from imageprocessing.capturingdevice import initialize_real_devices
from imageprocessing.draw import Draw

from services.cam_service import CamService
from services.calib_service import calibrate

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
        if len(args.DEVICE_IDS) > 1:
            log.error("Please provide one camera at a time to calibrate.")
            sys.exit()
        else:
            device_id = int(args.DEVICE_IDS[0])
        calibrate(device_id)

    elif args.MODE == "mytest":
        cam = CamService(0, 1280, 720)
        img = cam.draw_setup_lines()
        cv2.imshow("test", img)
        while True:
            cv2.imshow("test", img)
            c = cv2.waitKey(1)
            if 'q' == chr(c & 255):
                break
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

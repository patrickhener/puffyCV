#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import signal
import sys
import cv2

from puffyCV.args import args

from services.logging_service import initialize_logging
from services.calib_service import calibrate
from services.draw_service import Board, draw_banner, board_resolution
from services.config_service import return_config_as_device
from services.game_service import GameLoop
from services.testing_service import test_for_cams

log = initialize_logging()


def signal_handler(sig, frame):
    log.info("CTRL-C caught, exiting...")
    sys.exit()


def main():
    signal.signal(signal.SIGINT, signal_handler)
    if not args.OBANNER:
        print(draw_banner())
    if args.MODE == "run":
        log.info("puffyCV recognition started")
    elif args.MODE == "cal":
        if len(args.DEVICE_IDS) > 1:
            log.error("Please provide one camera at a time to calibrate. Exiting ...")
            sys.exit()
        else:
            device_id = int(args.DEVICE_IDS[0])
        calibrate(device_id)
    elif args.MODE == "camtest":
        result = test_for_cams()
        for key in result:
            if result[key]:
                log.info("Video Device with ID {} is an accessible camera".format(key))
            else:
                log.error("Video Device with ID {} is not an accessible camera".format(key))
        sys.exit()
    elif args.MODE == "runtest":
        cams = []
        for device in args.DEVICE_IDS:
            cams.append(return_config_as_device(device))
        game_loop = GameLoop(cams)
        game_loop.run()

    elif args.MODE == "drawprojection":
        draw = Board(board_resolution)
        while True:
            cv2.imshow("Board Projection Test", draw.projection_prepare())
            c = cv2.waitKey(1)
            if 'q' == chr(c & 255):
                break

    elif args.MODE == "bannertest":
        print(draw_banner())


    else:
        log.error("Invalid mode selected. Please refer to README. Exiting ...")

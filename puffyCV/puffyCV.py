#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import signal
import sys
import cv2

from puffyCV.args import args

from services.logging_service import initialize_logging
from services.calib_service import calibrate
from services.draw_service import Board, draw_banner
from services.device_service import WebCamCapturingDevice
from services.config_service import get_config
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
            cam_config = get_config(device)
            cam_service = WebCamCapturingDevice(cam_config.get("device_id"), cam_config.get("roi_pos_y"),
                                                cam_config.get("roi_height"), cam_config.get("surface_y"),
                                                cam_config.get("surface_center"), cam_config.get("threshold"),
                                                cam_config.get("fov"), cam_config.get("bull_distance"),
                                                cam_config.get("position"))
            cams.append(cam_service)

        game_loop = GameLoop(cams)
        game_loop.run()

    elif args.MODE == "drawprojection":
        draw = Board(900)
        while True:
            cv2.imshow("test", draw.projection_prepare())
            c = cv2.waitKey(1)
            if 'q' == chr(c & 255):
                break

    elif args.MODE == "bannertest":
        print(draw_banner())


    else:
        log.error("Invalid mode selected. Please refer to README. Exiting ...")

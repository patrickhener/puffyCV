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

from services.cam_service import CamService
from services.config_service import initialize_config, get_config, set_config

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


def nothing(x):
    pass


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
    elif args.MODE == "mycal":
        log.info("Initializing device")
        if not initialize_config(0):
            log.info("No config found, creating dummy one")
            cam = CamService(0, 500, 20, 600, 640)
        else:
            log.info("Config found, loading")
            cam = get_config(0)

        roi_pos_y = cam.roi_pos_y
        roi_height = cam.roi_height
        surface_y = cam.surface_y
        surface_center = cam.surface_center

        cv2.namedWindow("calibrate")
        cv2.createTrackbar("roi_pos_y", "calibrate", roi_pos_y, 720, nothing)
        cv2.createTrackbar("roi_height", "calibrate",roi_height, 200, nothing)
        cv2.createTrackbar("surface_y", "calibrate", surface_y, 720, nothing)
        cv2.createTrackbar("surface_center", "calibrate", surface_center, 1280, nothing)

        while True:
            img = cam.draw_setup_lines(roi_pos_y, roi_height, surface_y, surface_center)
            cv2.imshow("calibrate", img)
            roi_pos_y = cv2.getTrackbarPos("roi_pos_y", "calibrate")
            roi_height = cv2.getTrackbarPos("roi_height", "calibrate")
            surface_y = cv2.getTrackbarPos("surface_y", "calibrate")
            surface_center = cv2.getTrackbarPos("surface_center", "calibrate")
            c = cv2.waitKey(1)
            if 'q' == chr(c & 255):
                log.info("key q pressed, saving config")
                cam = CamService(0, roi_pos_y, roi_height, surface_y, surface_center)
                set_config(0, cam)
                log.info("config saved successful")
                break

    else:
        log.error("Invalid mode selected. Please refer to README.")

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import signal
import sys

import puffyCV.calibration
import puffyCV.recognition
from puffyCV.args import args
from puffyCV.logging import log
from puffyCV.gameloop import GameLoop
from config.config_repo import create_config, put_config_for_device, find_config_for_device
from imageprocessing.capturingdevice import WebCamCapturingDevice
from positioning.dartboard import Board

devices = []

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


def initialize_real_devices():
    for device_id in args.DEVICE_IDS:
        config_of_device = find_config_for_device(device_id)
        dartboard_level_from_config = 0
        if config_of_device is not None:
            dartboard_level_from_config = config_of_device[1]
        devices.append(WebCamCapturingDevice(device_id, dartboard_level_from_config))


def configure_devices():
    for device in devices:
        config_of_device = find_config_for_device(device.device_number)
        level_loaded_from_config = 0
        if config_of_device is not None:
            level_loaded_from_config = config_of_device[1]
        dartboard_level = device.configure(level_loaded_from_config)
        put_config_for_device(device.device_number, dartboard_level)


def main():
    signal.signal(signal.SIGINT, signal_handler)
    if args.MODE == "run":
        create_config()
        initialize_real_devices()
        game_loop = GameLoop(devices)
        game_loop.run()
    elif args.MODE == "cal":
        log.info("puffyCV calibration started")
        create_config()
        initialize_real_devices()
        configure_devices()
    elif args.MODE == "mytest":
        # pass
        board = Board()
        board.print()
        # sender.send_throw("20","3")
    elif args.MODE == "mytest2":
        pass
        # sender = ScoreboardConnector("127.0.0.1", "5000")
        # sender.send_next()

    else:
        print("Invalid mode selected. Please refer to README.")

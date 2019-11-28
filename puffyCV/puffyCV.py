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
        print("puffyCV recognition started")
        puffyCV.recognition.start_recognition()
    elif args.MODE == "cal":
        print("puffyCV calibration started")
        puffyCV.calibration.start_calibration()
    elif args.MODE == "mytest":
        create_config()
        initialize_real_devices()
        if args.config:
            configure_devices()
        else:
            game_loop = GameLoop(devices)
            game_loop.run()

    else:
        print("Invalid mode selected. Please refer to README.")

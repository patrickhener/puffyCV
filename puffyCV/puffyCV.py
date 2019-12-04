#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from imutils.video import VideoStream

import signal
import sys
import cv2
import time
import imutils

from puffyCV.args import args
from puffyCV.gameloop import GameLoop

from services.logging_service import initialize_logging
from services.calib_service import calibrate
from services.draw_service import Board
from services.device_service import WebCamCapturingDevice
from services.config_service import get_config

log = initialize_logging()


def signal_handler(sig, frame):
    log.info("CTRL-C caught, exiting...")
    sys.exit()


def compute(device_id):
    vs = VideoStream(src=device_id).start()
    time.sleep(2.0)
    first_frame = None
    while True:

        # grab the current frame and initialize the occupied/unoccupied
        # text
        frame = vs.read()

        if frame is None:
            break

        # convert it to grayscale, and blur it
        frame = imutils.resize(frame, width=500)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        # if the first frame is None, initialize it
        if first_frame is None:
            first_frame = gray
            continue

        # compute the absolute difference between the current frame and
        # first frame
        frame_delta = cv2.absdiff(first_frame, gray)
        thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]

        # dilate the thresholded image to fill in holes, then find contours
        # on thresholded image
        thresh = cv2.dilate(thresh, None, iterations=2)
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                                cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)

        # min area = size of contour to filter
        min_area = 500
        # loop over the contours
        for c in cnts:
            # if the contour is too small, ignore it
            if cv2.contourArea(c) < min_area:
                continue

            # compute the bounding box for the contour, draw it on the frame,
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # show the frame and record if the user presses a key
        cv2.imshow("Security Feed", frame)
        cv2.imshow("Thresh", thresh)
        cv2.imshow("Frame Delta", frame_delta)
        key = cv2.waitKey(1) & 0xFF

        # if the `q` key is pressed, break from the lop
        if key == ord("q"):
            break


def main():
    signal.signal(signal.SIGINT, signal_handler)
    if args.MODE == "run":
        log.info("puffyCV recognition started")
    elif args.MODE == "cal":
        if len(args.DEVICE_IDS) > 1:
            log.error("Please provide one camera at a time to calibrate. Exiting ...")
            sys.exit()
        else:
            device_id = int(args.DEVICE_IDS[0])
        calibrate(device_id)
    elif args.MODE == "mytest":
        cams = []
        for device in args.DEVICE_IDS:
            cam_config = get_config(device)
            cam_service = WebCamCapturingDevice(cam_config.get("device_id"), cam_config.get("roi_pos_y"),
                                                cam_config.get("roi_height"), cam_config.get("surface_y"),
                                                cam_config.get("surface_center"))
            cams.append(cam_service)

        game_loop = GameLoop(cams)
        game_loop.run()

    elif args.MODE == "mytest2":
        draw = Board(900)
        while True:
            cv2.imshow("test", draw.projection_prepare())
            c = cv2.waitKey(1)
            if 'q' == chr(c & 255):
                break

    elif args.MODE == "newrecog":
        for device in args.DEVICE_IDS:
            compute(device)

    else:
        log.error("Invalid mode selected. Please refer to README. Exiting ...")

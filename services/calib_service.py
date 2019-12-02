import sys
import cv2
from puffyCV.args import args
from services.config_service import initialize_config, get_config, set_config
from services.cam_service import CamService
from services.logging_service import initialize_logging

log = initialize_logging()


def nothing(x):
    pass


def calibrate(device_id):
    """
    :param device_id: identifier number of device [0-X]
    :type device_id: int
    :return: nothing
    """
    log.info("Initializing device")
    if not initialize_config(device_id):
        log.info("No config found, creating dummy one")
        cam = CamService(device_id, 500, 20, 600, 640)
    else:
        log.info("Config found, loading")
        cam_load = get_config(device_id)
        cam = CamService(cam_load.get("device_id"), cam_load.get("roi_pos_y"), cam_load.get("roi_height"),
                         cam_load.get("surface_y"), cam_load.get("surface_center"))

    roi_pos_y = cam.roi_pos_y
    roi_height = cam.roi_height
    surface_y = cam.surface_y
    surface_center = cam.surface_center

    cv2.namedWindow("calibrate")
    cv2.createTrackbar("roi_pos_y", "calibrate", roi_pos_y, 720, nothing)
    cv2.createTrackbar("roi_height", "calibrate", roi_height, 200, nothing)
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
            set_config(device_id, roi_pos_y, roi_height, surface_y, surface_center)
            log.info("config saved successful")
            break

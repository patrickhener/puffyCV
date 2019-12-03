from cv2 import namedWindow, createTrackbar, imshow, getTrackbarPos, waitKey
from services.config_service import initialize_config, get_config, set_config
from services.device_service import WebCamCapturingDevice
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
        log.info("No config found for device {}, creating dummy one".format(device_id))
        cam = WebCamCapturingDevice(device_id, 500, 20, 600, 640)
    else:
        log.info("Config found for device {}, loading".format(device_id))
        cam_load = get_config(device_id)
        cam = WebCamCapturingDevice(cam_load.get("device_id"), cam_load.get("roi_pos_y"), cam_load.get("roi_height"),
                                    cam_load.get("surface_y"), cam_load.get("surface_center"))

    log.info("To end calibration hit q")
    roi_pos_y = cam.roi_pos_y
    roi_height = cam.roi_height
    surface_y = cam.surface_y
    surface_center = cam.surface_center

    namedWindow("calibrate")
    createTrackbar("roi_pos_y", "calibrate", roi_pos_y, 720, nothing)
    createTrackbar("roi_height", "calibrate", roi_height, 200, nothing)
    createTrackbar("surface_y", "calibrate", surface_y, 720, nothing)
    createTrackbar("surface_center", "calibrate", surface_center, 1280, nothing)

    while True:
        img = cam.draw_setup_lines(roi_pos_y, roi_height, surface_y, surface_center)
        imshow("calibrate", img)
        roi_pos_y = getTrackbarPos("roi_pos_y", "calibrate")
        roi_height = getTrackbarPos("roi_height", "calibrate")
        surface_y = getTrackbarPos("surface_y", "calibrate")
        surface_center = getTrackbarPos("surface_center", "calibrate")
        c = waitKey(1)
        if 'q' == chr(c & 255):
            log.info("key q pressed, saving config for device {}".format(device_id))
            set_config(device_id, roi_pos_y, roi_height, surface_y, surface_center)
            log.info("config saved successful")
            break

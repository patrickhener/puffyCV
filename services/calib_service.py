import cv2
from services.config_service import initialize_config, get_config, set_config
from services.device_service import WebCamCapturingDevice
from services.logging_service import initialize_logging
from services.processor_service import ProcessedImage

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
        cam = WebCamCapturingDevice(device_id, 500, 20, 600, 640, 30, 85, 33, 9)
    else:
        log.info("Config found for device {}, loading".format(device_id))
        cam_load = get_config(device_id)
        cam = WebCamCapturingDevice(cam_load.get("device_id"), cam_load.get("roi_pos_y"), cam_load.get("roi_height"),
                                    cam_load.get("surface_y"), cam_load.get("surface_center"),
                                    cam_load.get("threshold"), cam_load.get("fov"), cam_load.get("bull_distance"),
                                    cam_load.get("position"))

    log.info("To end calibration hit q")
    roi_pos_y = cam.roi_pos_y
    roi_height = cam.roi_height
    surface_y = cam.surface_y
    surface_center = cam.surface_center
    fov = cam.fov
    bull_distance = cam.bull_distance
    position = cam.position

    cv2.namedWindow("calibrate")
    cv2.createTrackbar("roi_pos_y", "calibrate", roi_pos_y, 720, nothing)
    cv2.createTrackbar("roi_height", "calibrate", roi_height, 200, nothing)
    cv2.createTrackbar("surface_y", "calibrate", surface_y, 720, nothing)
    cv2.createTrackbar("surface_center", "calibrate", surface_center, 1280, nothing)
    cv2.createTrackbar("fov", "calibrate", fov, 180, nothing)
    cv2.createTrackbar("bull_distance_cm", "calibrate", bull_distance, 100, nothing)
    cv2.createTrackbar("position", "calibrate", position, 180, nothing)

    threshold = cam.threshold
    cv2.namedWindow("threshold")
    cv2.createTrackbar("threshold", "threshold", threshold, 255, nothing)

    while True:
        img = cam.draw_setup_lines(roi_pos_y, roi_height, surface_y, surface_center)
        cv2.imshow("calibrate", img)
        thres = cam.show_threshold(threshold)
        cv2.imshow("threshold", thres)
        roi_pos_y = cv2.getTrackbarPos("roi_pos_y", "calibrate")
        roi_height = cv2.getTrackbarPos("roi_height", "calibrate")
        surface_y = cv2.getTrackbarPos("surface_y", "calibrate")
        surface_center = cv2.getTrackbarPos("surface_center", "calibrate")
        fov = cv2.getTrackbarPos("fov", "calibrate")
        bull_distance = cv2.getTrackbarPos("bull_distance_cm", "calibrate")
        position = cv2.getTrackbarPos("position", "calibrate")
        threshold = cv2.getTrackbarPos("threshold", "threshold")
        c = cv2.waitKey(1)
        if 'q' == chr(c & 255):
            log.info("key q pressed, saving config for device {}".format(device_id))
            set_config(device_id, roi_pos_y, roi_height, surface_y, surface_center, threshold, fov, bull_distance,
                       position)
            log.info("config saved successful")
            break

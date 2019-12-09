import numpy as np
import math

pi = np.pi


def find_angle(point1, point2):
    return math.atan2(point2[1] - point1[1], point2[0] - point1[0])


def calibrate_cam_setup_point(device, projection_center_point):
    start_rad_sector = pi * -1
    rad_sector_step = pi / 10
    dartboard_diameter_pixels = 800
    dartboard_diameter_in_cm = 34
    to_cam_distance = device.bull_distance
    to_cam_pixels = dartboard_diameter_pixels * to_cam_distance / dartboard_diameter_in_cm
    i = 1
    if device.position == 9:
        i = 2
    elif device.position == 5:
        i = 4
    elif device.position == 1:
        i = 6
    elif device.position == 4:
        i = 8
    calibrated_cam_setup_point = [int(projection_center_point[0] + math.cos(start_rad_sector + i * rad_sector_step) *
                                      to_cam_pixels),
                                  int(projection_center_point[1] + math.sin(start_rad_sector + i * rad_sector_step) *
                                      to_cam_pixels)]

    return calibrated_cam_setup_point


def ray_projection(processed_image, device):
    if processed_image is not None:
        line = processed_image.darts_axis
        if line is not None:
            # TODO projection ray
            # add ray line to projection/call projection routine
            # 1. Translate cam surface POI to dartboard projection
            projection_center_point = (device.resolution_width / 2, device.resolution_height / 2)
            x_value = int(processed_image.bounding_box.x +
                          processed_image.darts_axis[len(processed_image.darts_axis) - 1])

            frame_width = device.resolution_width
            frame_semi_width = frame_width / 2
            cam_fov = device.fov
            cam_fov_semi_angle = cam_fov / 2
            projection_to_center = [0, 0]
            surface_poi_to_center_distance = processed_image.darts_board_center - x_value
            if surface_poi_to_center_distance < 0:
                surface_poi_to_center_distance *= -1
            projection_cam_to_center_distance = frame_semi_width / math.sin(pi * cam_fov_semi_angle / 180.0) * \
                                                math.pow(surface_poi_to_center_distance, 2)
            projection_cam_to_poi_distance = math.sqrt(math.pow(projection_cam_to_center_distance, 2) +
                                                       math.pow(surface_poi_to_center_distance, 2))
            projection_poi_to_center_distance = math.sqrt(math.pow(projection_cam_to_poi_distance, 2) -
                                                          math.pow(projection_cam_to_center_distance, 2))
            poi_cam_center_angle = math.asin(projection_poi_to_center_distance / projection_cam_to_poi_distance)
            cam_setup_point = calibrate_cam_setup_point(device, projection_center_point)
            cam_to_bull_angle = find_angle(cam_setup_point, projection_center_point)

            projection_to_center[0] = cam_setup_point[0] - math.cos(cam_to_bull_angle) * \
                                     projection_cam_to_center_distance
            projection_to_center[1] = cam_setup_point[0] - math.sin(cam_to_bull_angle) * \
                                     projection_cam_to_center_distance

            projection_poi = [0, 0]
            projection_poi[0] = cam_setup_point[0] + math.cos(cam_to_bull_angle + poi_cam_center_angle)
            projection_poi[1] = cam_setup_point[1] + math.sin(cam_to_bull_angle + poi_cam_center_angle)

            # 2. Draw line from cam through projection POI
            ray_point = projection_poi
            angle = find_angle(cam_setup_point, ray_point)
            ray_point[0] = int(cam_setup_point[0] + math.cos(angle) * 2000)
            ray_point[1] = int(cam_setup_point[1] + math.sin(angle) * 2000)

            return tuple(cam_setup_point), tuple(ray_point)

import time
import asyncio
import cv2
import math
import numpy as np

from services.detector_service import has_new_images
from services.processor_service import erode, segment, find_darts_axis
from services.data_service import ProcessedImage
from services.display_service import display_with_information, display_board
from services.draw_service import Board, draw_line

pi = np.pi


def process_input(processed_image, threshold):
    processed_image.image = erode(processed_image, threshold)
    processed_image.set_bounding_box(segment(processed_image, threshold))
    processed_image.set_darts_axis(find_darts_axis(processed_image))
    display_with_information(processed_image)


def find_angle(point1, point2):
    return math.atan2(point2.y - point1.y, point2.x - point1.x)


class GameLoop:
    """
    GameLoop controls the application flow. It provides the clock speed of the application by setting a frame rate
    for the capturing devices. While running, the game loop queries the devices in the resulting time periods and
    delegates the results from the capturing devices to the processing functions.
    """

    def __init__(self, devices):
        """
        :param devices: capturing devices (e.g. web cams) for capturing visual input
        :type devices: list of CapturingDevice
        """
        self.devices = devices
        self.capturing = True

    def run(self):
        """
        runs the game loop as asynchronous task
        """
        asyncio.run(self.async_run())

    async def async_run(self):
        """
        asynchronous task
        """

        while self.capturing:
            self.process()

        # When everything done, release the capture devices
        for captured_input in self.devices:
            captured_input.release()

        cv2.destroyAllWindows()

    def process(self):
        # First initialize projection
        board = Board(800).projection_prepare()
        for device in self.devices:
            device.process_image()

        if has_new_images(self.devices):
            for device in self.devices:
                latest_frame = device.fetch_latest_frame()
                if not latest_frame.all():
                    # set image and image metadata
                    processed_image = ProcessedImage(latest_frame,
                                                     device.resolution_width,
                                                     device.resolution_height,
                                                     device.device_id)
                    # set the dart board level obtained from the device
                    processed_image.set_darts_board_offset(device.surface_y, device.surface_center)
                    processed_image.set_roi_offset(device.roi_pos_y, device.roi_height)
                    # do image processing and display one output window per device
                    process_input(processed_image, device.threshold)
                    # TODO projection ray
                    # add ray line to projection/call projection routine
                    # 1. Translate cam surface POI to dartboard projection
                    x_value = int(processed_image.bounding_box.x + processed_image.darts_axis[len(processed_image.darts_axis) - 1])
                    frame_width = device.resolution_width
                    frame_semi_width = frame_width / 2
                    cam_fov = 85  # TODO This has to be in calibration routine/config pickle of device
                    cam_fov_semi_angle = cam_fov / 2
                    projection_to_center = (0, 0)
                    surface_poi_to_center_distance = processed_image.darts_board_center - x_value
                    if surface_poi_to_center_distance < 0:
                        surface_poi_to_center_distance *= -1
                    projection_cam_to_center_distance = frame_semi_width / math.sin(pi * cam_fov_semi_angle / 180.0) * math.pow(surface_poi_to_center_distance, 2)
                    projection_cam_to_poi_distance = math.sqrt(math.pow(projection_cam_to_center_distance, 2) + math.pow(surface_poi_to_center_distance, 2))
                    projection_poi_to_center_distance = math.sqrt(math.pow(projection_cam_to_poi_distance, 2) - math.pow(projection_cam_to_center_distance, 2))
                    poi_cam_center_angle = math.asin(projection_poi_to_center_distance / projection_cam_to_poi_distance)
                    cam_setup_point = (0, 0)  # TODO find setup point look at YellowFive5 - tweak calibration
                    cam_to_bull_angle = 0  # TODO find cam to bull angle look at YellowFive5 - tweak calibration

                    projection_to_center.x = cam_setup_point.x - math.cos(cam_to_bull_angle) * projection_cam_to_center_distance
                    projection_to_center.y = cam_setup_point.x - math.sin(cam_to_bull_angle) * projection_cam_to_center_distance

                    projection_poi = (0, 0)
                    projection_poi.x = cam_setup_point.x + math.cos(cam_to_bull_angle + poi_cam_center_angle)
                    projection_poi.y = cam_setup_point.y + math.sin(cam_to_bull_angle + poi_cam_center_angle)

                    # 2. Draw line from cam through projection POI
                    ray_point = projection_poi
                    angle = find_angle(cam_setup_point, ray_point)
                    ray_point.x = cam_setup_point.x + math.cos(angle) * 2000
                    ray_point.y = cam_setup_point.y + math.sin(angle) * 2000
                    board.draw_line(cam_setup_point, ray_point)

            # display board
            display_board(board)


